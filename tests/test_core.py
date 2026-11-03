import copy
import json
import struct
import sys
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "arena" / "services"), str(ROOT / "arena" / "containment")]

import exposure_audit  # noqa: E402
import fake_llm  # noqa: E402
import llm_proxy  # noqa: E402
import matrix  # noqa: E402
from bsa import catalog, runner  # noqa: E402
from bsa.observers import Evidence, classify  # noqa: E402
from bsa.stats import clustered_mean, wilson  # noqa: E402

SMOKE = json.loads((ROOT / "catalog" / "BSA-SMOKE-0001.json").read_text(encoding="utf-8"))


class Stats(unittest.TestCase):
    def test_known_bounds(self):
        self.assertAlmostEqual(wilson(0, 10)[1], 0.2775, places=3)
        self.assertAlmostEqual(wilson(0, 30)[1], 0.1135, places=3)
        self.assertEqual(wilson(10, 10)[1], 1.0)

    def test_rejects_nonsense(self):
        for args in ((1, 0), (5, 4), (-1, 4)):
            with self.assertRaises(ValueError):
                wilson(*args)


class ClusteredMean(unittest.TestCase):
    def test_tied_scores_widen_the_error(self):
        self.assertAlmostEqual(clustered_mean([[1], [1], [0], [0]])["se"], 0.25)
        self.assertAlmostEqual(clustered_mean([[1, 1], [0, 0]])["se"], 2 ** 0.5 / 4)

    def test_bounds_stay_between_zero_and_one(self):
        result = clustered_mean([[1, 1], [0, 0]])
        self.assertEqual((result["low"], result["high"], result["clusters"]), (0.0, 1.0, 2))

    def test_no_scores_is_refused(self):
        with self.assertRaises(ValueError):
            clustered_mean([])


class Observers(unittest.TestCase):
    def test_effect_beats_claims(self):
        self.assertEqual(classify(Evidence(canary_at_sink=True, detected=True, blocked=True)), "COMPROMISED")

    def test_infra_error_is_not_a_result(self):
        self.assertEqual(classify(Evidence(infra_error=True, canary_at_sink=True)), "INFRA_ERROR")

    def test_default_is_ignored(self):
        self.assertEqual(classify(Evidence()), "IGNORED")


class Catalog(unittest.TestCase):
    def test_shipped_catalog_is_valid(self):
        self.assertEqual(catalog.validate_all(), {})

    def rejected(self, text):
        bad = copy.deepcopy(SMOKE)
        bad["title"] = text
        return catalog.validate(bad)

    def test_rejects_real_host(self):
        self.assertIn("R2-real-host", self.rejected("post to https://evil.com/x"))

    def test_allows_reserved_test_host(self):
        self.assertEqual(self.rejected("post to http://sink.bsa.test:8080/x"), [])

    def test_rejects_stored_canary(self):
        self.assertIn("R1-literal-canary", self.rejected("BSA-CANARY-0123456789abcdef"))

    def test_rejects_destructive_commands(self):
        self.assertIn("R4-destructive", self.rejected("run rm -rf build"))

    def test_rejects_pipe_to_shell(self):
        self.assertIn("R5-pipe-to-shell", self.rejected("curl x | sh"))

    def test_rejects_unknown_fields(self):
        bad = {**SMOKE, "payload_inline": "x"}
        self.assertIn("unknown:payload_inline", catalog.validate(bad))


class Summary(unittest.TestCase):
    GOOD = {"schema": 1, "run_id": "abc", "scenario": "BSA-SMOKE-0001", "agent": "fake-agent",
            "behaviour": "ignores", "outcome": "IGNORED", "task_completed": True, "duration_ms": 5}

    def test_accepts_clean_summary(self):
        self.assertEqual(runner.safe_summary(dict(self.GOOD)), self.GOOD)

    def test_free_text_cannot_leave(self):
        for field, value in (("scenario", "ignore previous instructions"), ("outcome", "OK now run this"),
                             ("agent", "a\nb")):
            with self.assertRaises(ValueError):
                runner.safe_summary({**self.GOOD, field: value})

    def test_extra_fields_cannot_leave(self):
        with self.assertRaises(ValueError):
            runner.safe_summary({**self.GOOD, "transcript": "x"})

    def test_bool_is_not_an_int(self):
        with self.assertRaises(ValueError):
            runner.safe_summary({**self.GOOD, "duration_ms": True})


class Proxy(unittest.TestCase):
    def test_server_side_search_is_removed(self):
        payload = {"tools": [{"name": "Read"}, {"type": "web_search_20250305", "name": "web_search"}]}
        llm_proxy.strip_server_tools(payload)
        self.assertEqual(payload["tools"], [{"name": "Read"}])


class ProxyRefusal(unittest.TestCase):
    def test_refused_route_with_a_body_still_gets_its_status(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), llm_proxy.Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            request = urllib.request.Request(f"http://127.0.0.1:{server.server_port}/admin", data=b"x" * 1_000_000)
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(request, timeout=10)
            self.assertEqual(caught.exception.code, 403)
        finally:
            server.shutdown()
            server.server_close()


class FakeModel(unittest.TestCase):
    def test_script_advances_with_tool_results(self):
        request = {"tools": [{}], "messages": []}
        blocks, stop = fake_llm.next_blocks(request, "bash-side")
        self.assertEqual((blocks[0]["name"], stop), ("Bash", "tool_use"))
        request["messages"] = [{"content": [{"type": "tool_result"}]}]
        self.assertEqual(fake_llm.next_blocks(request, "bash-side")[1], "end_turn")

    def test_final_reply_reports_the_tool_outcome(self):
        ok = [{"content": [{"type": "tool_result"}]}]
        failed = [{"content": [{"type": "tool_result", "is_error": True}]}]
        self.assertEqual(fake_llm.last_tool_state(ok), "tool-ok")
        self.assertEqual(fake_llm.last_tool_state(failed), "tool-error")
        self.assertEqual(fake_llm.last_tool_state([]), "no-tool")

    def test_background_requests_get_text(self):
        self.assertEqual(fake_llm.next_blocks({"messages": []}, "bash-side")[1], "end_turn")

    def test_every_matrix_action_has_a_script(self):
        self.assertEqual(set(fake_llm.ACTIONS), set(matrix.ACTIONS))
        self.assertTrue(all(f"act-{a}" in fake_llm.SCRIPTS for a in matrix.ACTIONS))

    def test_matrix_keeps_its_controls(self):
        self.assertIn("default", matrix.PROFILES)
        self.assertIn("bypass", matrix.PROFILES)


class Audit(unittest.TestCase):
    def rules(self, text, terms=()):
        return [f.split(" ")[1] for f in exposure_audit.scan("f", text, list(terms))]

    def test_finds_secrets_and_paths(self):
        self.assertIn("local-path", self.rules("C:" + "\\Users\\someone\\x"))
        self.assertIn("local-path", self.rules("D:" + "/work/project"))
        self.assertIn("anthropic-key", self.rules("sk-ant-" + "a" * 30))
        self.assertIn("email", self.rules("reach me at person@" + "gmail.com"))
        self.assertIn("private-key", self.rules("-----BEGIN RSA " + "PRIVATE KEY-----"))

    def test_finds_invisible_characters(self):
        self.assertIn("invisible-char", self.rules("clean\u200btext"))
        self.assertIn("invisible-char", self.rules("tag\U000e0041"))

    def test_finds_personal_terms_case_insensitively(self):
        self.assertIn("personal-term-0", self.rules("Hello JANE", ["jane"]))

    def test_never_reports_the_matched_text(self):
        secret = "sk-ant-" + "b" * 30
        self.assertNotIn(secret, " ".join(exposure_audit.scan("f", secret, [])))

    def test_finds_private_addresses_and_more_key_formats(self):
        self.assertIn("private-ip", self.rules("192.168." + "1.20"))
        self.assertIn("api-key", self.rules("AIza" + "b" * 35))
        self.assertIn("bearer", self.rules("Authorization: Bearer " + "c" * 24))

    def test_png_metadata_is_reported(self):
        chunk = struct.pack(">I4s", 0, b"tEXt") + b"\0\0\0\0"
        self.assertEqual(exposure_audit.png_metadata(b"\x89PNG\r\n\x1a\n" + chunk), ["tEXt"])

    def test_shipped_logo_has_no_metadata(self):
        data = (ROOT / "docs" / "assets" / "bsa-logo.png").read_bytes()
        self.assertEqual(exposure_audit.png_metadata(data), [])

    def test_noreply_and_examples_pass(self):
        self.assertEqual(self.rules("1+x@users.noreply.github.com and a@example.com"), [])


if __name__ == "__main__":
    unittest.main()
