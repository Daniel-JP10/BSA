"""PreToolUse hook used by the contract tests.

A flag file selects the decision, so each test decides whether this level of
settings acts. Without a flag the hook stays silent.
Usage: deny_hook.py <level>, with flag /tmp/bsa-<level> holding "deny" or "ask".
"""
import json
import sys
from pathlib import Path

flag = Path(f"/tmp/bsa-{sys.argv[1]}")
if flag.exists():
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": flag.read_text().strip(),
        "permissionDecisionReason": "bsa contract",
    }}))
