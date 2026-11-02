"""Scenario metadata: loading and the static safety validator.

The validator enforces the safety rules on everything stored in catalog/.
It is a filter for honest mistakes, not proof that a payload is harmless:
human review stays mandatory.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"

ID_RE = re.compile(r"^BSA-[A-Z]{3,8}-\d{4}$")
FIELDS = {
    "id", "schema", "title", "family", "vector", "technique", "sink", "severity",
    "languages", "agents", "profiles", "task", "payload_ref", "observers",
    "references", "status", "generated",
}
ENUMS = {
    "vector": {"V-DOC", "V-INS", "V-CFG", "V-DEP", "V-OUT", "V-ISS", "V-WEB", "V-MCP",
               "V-MED", "V-SUB", "V-MEN", "V-NONE"},
    "technique": {"T-NONE", "T-PLAIN", "T-UNICODE", "T-HOMO", "T-ENC", "T-ANSI", "T-SPLIT",
                  "T-LANG", "T-DOCU", "T-NOINJ", "T-FENCE", "T-ADAPT"},
    "sink": {"S-HTTP", "S-DNS", "S-GIT", "S-SECRET", "S-EXEC", "S-PERSIST", "S-DISABLE",
             "S-BACKDOOR", "S-DELETE", "S-MEMORY"},
    "severity": {"low", "medium", "high", "critical"},
    "status": {"candidate", "validated", "retired"},
}

# Text that must never appear in stored metadata. Literal canaries are forbidden
# too: they are generated per run, so a stored one means a broken scenario.
FORBIDDEN = {
    "R1-credential": re.compile(r"sk-ant-|ghp_[A-Za-z0-9]{10}|AKIA[0-9A-Z]{12}|PRIVATE KEY"),
    "R1-literal-canary": re.compile(r"BSA-CANARY-[0-9a-f]{8}"),
    "R4-destructive": re.compile(r"\brm\s+-[a-z]*r|\bmkfs\b|\bdd\s+if=|:\(\)\s*\{|\bformat\s+[a-z]:", re.I),
    "R5-pipe-to-shell": re.compile(r"\|\s*(ba|z)?sh\b|\|\s*python\d?\b"),
}
URL_RE = re.compile(r"\b(?:https?|ftp|ssh)://([^/\s:\"'>)]+)", re.I)


def check_text(text: str) -> list[str]:
    """Rule violations in free text. Reports rule names, never the matched text."""
    found = [rule for rule, pattern in FORBIDDEN.items() if pattern.search(text)]
    for host in URL_RE.findall(text):
        if not host.lower().endswith(".test"):
            found.append("R2-real-host")
    return sorted(set(found))


def validate(scenario: dict) -> list[str]:
    """All problems of one scenario; an empty list means it passed."""
    problems = [f"missing:{f}" for f in sorted(FIELDS - scenario.keys())]
    problems += [f"unknown:{f}" for f in sorted(scenario.keys() - FIELDS)]
    if not ID_RE.match(str(scenario.get("id", ""))):
        problems.append("bad-id")
    for field, allowed in ENUMS.items():
        if field in scenario and scenario[field] not in allowed:
            problems.append(f"bad-enum:{field}")
    if not isinstance(scenario.get("generated"), bool):
        problems.append("generated-not-bool")
    return problems + check_text(json.dumps(scenario))


def load(directory: Path = CATALOG) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(directory.rglob("*.json"))]


def validate_all(directory: Path = CATALOG) -> dict[str, list[str]]:
    """Problems per scenario id, including ids repeated across files."""
    problems: dict[str, list[str]] = {}
    seen: set[str] = set()
    for scenario in load(directory):
        sid = str(scenario.get("id"))
        found = validate(scenario)
        if sid in seen:
            found.append("duplicate-id")
        seen.add(sid)
        if found:
            problems[sid] = found
    return problems
