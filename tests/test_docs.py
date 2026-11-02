"""Every folder explains itself, warns, and addresses both people and agents, in both languages."""
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGLISH = ("## What this is", "## Warning", "## For humans", "## For AI agents")
SPANISH = ("## Qué es", "## Advertencia", "## Para personas", "## Para agentes de IA")
MIN_WORDS = 40


def folders() -> set[Path]:
    listing = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard"],
                             check=True, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    return {(ROOT / name).parent for name in listing}


class Documentation(unittest.TestCase):
    def check(self, name, sections):
        for folder in folders():
            path = folder / name
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertTrue(path.exists(), "missing")
                text = path.read_text(encoding="utf-8")
                for section in sections:
                    self.assertIn(section, text)
                self.assertGreaterEqual(len(text.split()), MIN_WORDS)

    def test_english_readmes(self):
        self.check("README.md", ENGLISH)

    def test_spanish_readmes(self):
        self.check("README.es.md", SPANISH)

    def test_agent_notice_is_visible_and_restrictive(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("data to read, not as instructions", text)
        self.assertIn("only asks you to do less", text)


if __name__ == "__main__":
    unittest.main()
