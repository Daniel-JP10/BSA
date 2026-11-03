import io
import re
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]

from bsa import published  # noqa: E402
from test_xlsx import make_xlsx  # noqa: E402

HEADER = list(published.COLUMNS)


def run_row(agent="Cursor", vector="PDF", perturbation="Top", eem=1, issue="SymPy #1", category="Supply Chain",
            model="Sonnet 4.6"):
    return [issue, category, agent, model, vector, perturbation, eem, None if eem else "Model Refusal"]


def archive(sheets: dict[str, list[list]], name="results/X_Results_final.xlsx") -> io.BytesIO:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        z.writestr(name, make_xlsx(sheets))
    out.seek(0)
    return out


def combination(agent, alt_text_succeeds=False):
    """One combination: two perturbations on a normal vector and two on image alt-text."""
    rows = [run_row(agent, "PDF", p) for p in ("Top", "Middle")]
    rows += [run_row(agent, "Image Alt-text", p, eem=int(alt_text_succeeds)) for p in ("Top", "Middle")]
    return rows


class Reading(unittest.TestCase):
    def test_reads_runs_and_skips_the_metrics_sheet(self):
        sheets = {"Metrics": [["METRICS"]], "Issue #1": [HEADER, run_row(), run_row(eem=0)]}
        rows = published.read_runs(archive(sheets))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]["Rejection_Attribution"], "Model Refusal")

    def test_unexpected_columns_are_refused(self):
        with self.assertRaises(ValueError):
            published.read_runs(archive({"Issue #1": [["a", "b"], ["x", "y"]]}))

    def test_eem_must_be_zero_or_one(self):
        with self.assertRaises(ValueError):
            published.read_runs(archive({"Issue #1": [HEADER, run_row(eem=2)]}))

    def test_archive_without_results_is_refused(self):
        with self.assertRaises(ValueError):
            published.read_runs(archive({"Issue #1": [HEADER]}, name="other/file.xlsx"))

    def test_expected_checksum_looks_like_an_md5(self):
        self.assertRegex(published.EXPECTED_MD5, r"^[0-9a-f]{32}$")


class Summary(unittest.TestCase):
    def rows(self, extra=()):
        data = combination("Cursor") + combination("Claude Code") + list(extra)
        return [dict(zip(published.COLUMNS, r)) for r in data]

    def test_counts_and_repeated_configurations(self):
        s = published.summarize(self.rows())
        self.assertEqual((s["runs"], s["distinct_configurations"], s["repeated_configurations"]), (8, 8, 0))
        self.assertEqual(s["successes"], 4)

    def test_a_repeated_configuration_is_reported(self):
        s = published.summarize(self.rows(extra=[run_row("Cursor", "PDF", "Top")]))
        self.assertEqual(s["repeated_configurations"], 1)

    def test_combinations_are_the_unit(self):
        s = published.summarize(self.rows())
        self.assertEqual(s["combinations"]["total"], 2)
        self.assertEqual(s["combinations"]["shape"], {"mixed": 2})
        self.assertEqual(s["mixed_combinations_by_vector"]["Image Alt-text"], {"successes": 0, "runs": 4})
        self.assertEqual(s["mixed_combinations_by_vector"]["PDF"], {"successes": 4, "runs": 4})

    def test_same_model_across_products(self):
        s = published.summarize(self.rows())["same_model_across_products"]["Sonnet 4.6"]
        self.assertEqual((s["paired_runs"], s["same_outcome"]), (4, 4))
        self.assertEqual(s["products"], ["Claude Code", "Cursor"])

    def test_products_that_disagree_are_counted(self):
        data = combination("Cursor") + combination("Claude Code", alt_text_succeeds=True)
        s = published.summarize([dict(zip(published.COLUMNS, r)) for r in data])
        self.assertEqual(s["same_model_across_products"]["Sonnet 4.6"]["same_outcome"], 2)

    def test_claude_code_slice_uses_combinations(self):
        cc = published.summarize(self.rows())["claude_code"]
        self.assertEqual((cc["combinations"], cc["combinations_with_a_success"]), (1, 1))
        self.assertEqual(cc["by_attack_category"]["Supply Chain"], {"successes": 2, "runs": 4})

    def test_clustered_rate_uses_combinations(self):
        s = published.summarize(self.rows())
        row = s["clustered_by_agent_and_model"]["Claude Code + Sonnet 4.6"]
        self.assertEqual((row["mean"], row["clusters"], row["items"]), (0.5, 1, 4))
        self.assertEqual(s["claude_code"]["clustered_over_runs"]["clusters"], 1)

    def test_render_is_text_with_the_headline(self):
        text = published.render(published.summarize(self.rows()))
        self.assertIn("runs: 8", text)
        self.assertIn("same model, different products", text)
        self.assertFalse(re.search(r"Traceback", text))


if __name__ == "__main__":
    unittest.main()
