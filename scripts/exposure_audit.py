"""Pre-publication audit. Nothing should be pushed until this passes.

Scans the files Git would publish and the whole commit history, including messages.
Reports rule and location, never the matched text. It is run by hand: nothing
enforces it. List personal terms in .bsa-audit-terms (gitignored), one per line,
so the names being searched for are not themselves published.
"""
import re
import struct
import subprocess
import sys
import unicodedata
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from bsa.catalog import check_text  # noqa: E402

PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+-]+@(?!example\.(?:com|org|net)\b|users\.noreply\.github\.com)"
                        r"[A-Za-z0-9-]+\.[A-Za-z]{2,}"),
    "local-path": re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]+[A-Za-z]|\\\\[A-Za-z0-9.-]+\\[A-Za-z]|/Users/[A-Za-z]"
                             r"|/home/(?!agent\b|dev\b)[A-Za-z]|/roo[t]/"),
    "private-ip": re.compile(r"\b(?:10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)\b"),
    "machine-name": re.compile(r"\b(?:DESKTOP|LAPTOP)-[A-Z0-9]{5,}\b"),
    "anthropic-key": re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    "api-key": re.compile(r"\bsk-[A-Za-z0-9_-]{32,}|\bAIza[0-9A-Za-z_-]{30,}|\bhf_[A-Za-z0-9]{30,}|\bnpm_[A-Za-z0-9]{30,}"
                          r"|\bglpat-[A-Za-z0-9_-]{20,}|\b[rs]k_live_[A-Za-z0-9]{20,}"),
    "github-token": re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}"),
    "aws-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "slack-token": re.compile(r"xox[bpras]-[A-Za-z0-9-]{20,}"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\."),
    "bearer": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._-]{20,}"),
    "private-key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "assigned-secret": re.compile(r"(?i)(api[_-]?key|secret|password|passwd)\s*[:=]\s*['\"]?[A-Za-z0-9/+_-]{20,}"),
}
# Docker's documented bridge gateway, tested on purpose by the containment checks.
ALLOWED_PRIVATE_IP = "172.17.0.1"
FORBIDDEN_FILES = (".env", ".env.*", "*.pem", "*.key", "id_rsa*", "id_ed25519*", "id_ecdsa*", "*.jsonl", "credentials*",
                   "*.p12", "*.pfx", "*.sqlite", "*.db", ".npmrc", ".pypirc", ".netrc", ".git-credentials", "*.kdbx",
                   "*.ppk", "*.sql", "*.zip", "*.log", "settings.local.json")
# Image data and display settings only: text, EXIF and timestamps stay forbidden.
PNG_CHUNKS = {"IHDR", "PLTE", "IDAT", "IEND", "sRGB", "gAMA", "pHYs"}
HIDDEN_CATEGORIES = {"Cf", "Cc", "Co", "Cn", "Zl", "Zp"}
HIDDEN_LOOKALIKES = (0x034F, 0x115F, 0x1160, 0x3164)
MAX_FILE = 2_000_000


def publishable() -> list[str]:
    args = ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard"]
    return subprocess.run(args, check=True, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()


def hidden_character(c: str) -> bool:
    code = ord(c)
    return (c != "\t" and unicodedata.category(c) in HIDDEN_CATEGORIES) or code in HIDDEN_LOOKALIKES \
        or 0xFE00 <= code <= 0xFE0F or 0xE0100 <= code <= 0xE01EF


def scan(name: str, text: str, terms: list[str]) -> list[str]:
    found = []
    for number, line in enumerate(text.split("\n"), 1):
        for rule, pattern in PATTERNS.items():
            if pattern.search(line.replace(ALLOWED_PRIVATE_IP, "")):
                found.append(f"{name}:{number} {rule}")
        if any(hidden_character(c) for c in line):
            found.append(f"{name}:{number} invisible-char")
        lowered = unicodedata.normalize("NFC", line).lower()
        for index, term in enumerate(terms):
            if term in lowered:
                found.append(f"{name}:{number} personal-term-{index}")
    return found


def png_metadata(data: bytes) -> list[str]:
    """Chunk types beyond what an image needs in order to display."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return ["not-a-png"]
    extra, index = set(), 8
    while index < len(data):
        size, kind = struct.unpack(">I4s", data[index:index + 8])
        extra.add(kind.decode("latin-1"))
        index += 12 + size
    return sorted(extra - PNG_CHUNKS)


def load_terms() -> list[str]:
    path = ROOT / ".bsa-audit-terms"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    return [unicodedata.normalize("NFC", t.strip()).lower() for t in lines if t.strip()]


def audit_history(terms: list[str]) -> list[str]:
    args = ["git", "-C", str(ROOT), "log", "--all", "-p", "--format=commit %h%n%B", "--no-color"]
    done = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if done.returncode:  # a repository with no commits has no history to scan
        return []
    keep = (line[1:] if line[:1] in ("+", "-") else line for line in done.stdout.splitlines())
    return [f.replace("h:", "history:", 1) for f in scan("h", "\n".join(keep), terms)]


def audit(terms: list[str]) -> list[str]:
    findings = []
    names = publishable()
    if any(n.startswith("proyecto/") for n in names):
        findings.append("proyecto/ is publishable: .gitignore is broken")
    for name in names:
        path = ROOT / name
        if any(fnmatch(path.name, pattern) for pattern in FORBIDDEN_FILES):
            findings.append(f"{name} forbidden-file")
        if path.stat().st_size > MAX_FILE:
            findings.append(f"{name} too-large")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            if name.startswith("docs/assets/") and name.endswith(".png"):
                findings += [f"{name} png-chunk-{kind}" for kind in png_metadata(path.read_bytes())]
            else:
                findings.append(f"{name} binary-file")
            continue
        findings += scan(name, text, terms)
        if name.startswith("catalog/"):
            findings += [f"{name} {rule}" for rule in check_text(text)]
    return findings + audit_history(terms)


if __name__ == "__main__":
    personal = load_terms()
    results = audit(personal)
    for line in results:
        print("FAIL", line)
    if not personal:
        print("WARN no personal terms loaded: names and usernames were not searched")
    print(f"{len(publishable())} files and full history scanned, {len(personal)} personal terms, "
          f"{len(results)} findings")
    sys.exit(1 if results else 0)
