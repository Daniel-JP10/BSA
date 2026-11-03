# Threat model

[Español](THREAT_MODEL.es.md)

Defences marked planned protect a catalog that does not exist yet.

## What BSA evaluates

| Element | Definition |
|---|---|
| Attacker | Controls content the agent will read, but not the machine or the account |
| Victim | A coding agent with access to files, a terminal and a network |
| Simulated assets | Canary secrets, code and agent configuration |
| Out of scope | An attacker already on the machine, a malicious user, failures of the model provider |

## What threatens BSA itself

| Threat | Who is at risk | Main defense | Status |
|---|---|---|---|
| An attack escapes the arena | The operator | Internal network, no host mounts, containment tests | In place |
| The agent steals the API key | The operator | The key stays in the proxy | Planned, no key is used today |
| An agent visiting the repository obeys an attack | The visitor | Payloads inert at rest, not stored as readable text | Planned |
| An agent reads results containing attacks | The analyst | Only typed fields leave the arena | In place for the fake agent |
| A pull request adds a harmful payload | The community | Validator and mandatory human review | Validator in place, review is a policy |
| CI runs attacks with secrets available | The project | No secrets on pull requests from forks | Planned, there is no CI yet |
| The catalog is reused against third parties | Third parties | Canaries and destinations valid only in the arena | Planned |
| A compromised dependency or image | Everyone | Python standard library only, base images pinned by digest, agent pinned by version. System packages are not pinned | In place |
| A new flaw is published without warning the vendor | Third parties | Coordinated disclosure | Policy |

## Why the controls matter: published incidents

Each of these records describes a confirmation, trust or isolation control in a coding agent that failed until a later version fixed it. Facts are from the records [R21]. BSA has not reproduced them. It tests only Claude Code, at versions later than every Claude Code fix listed here.

| Record | Product | Affected | Weakness | What the record says | Published |
|---|---|---|---|---|---|
| CVE-2025-55284 | Claude Code | Before 1.0.4 | CWE-78 | Confirmation prompts could be bypassed because of an overly broad allowlist of safe commands | 2025-08-16 |
| CVE-2025-54135 | Cursor | Below 1.3.9 | CWE-78, CWE-829 | Creating a new dotfile in the workspace did not require approval | 2025-08-05 |
| CVE-2025-61591 | Cursor | 1.7 and below | CWE-78 | An untrusted MCP server could return injected commands during OAuth setup | 2025-10-03 |
| CVE-2025-62222 | VS Code Copilot Chat extension | See the record | CWE-20, CWE-77 | Command injection allowing code execution over a network | 2025-11-11 |
| CVE-2025-65099 (GHSA-5hhx-v7f6-x7gv) | Claude Code | Before 1.0.39 | CWE-94 | Command execution before the startup trust dialog | 2025-11-19 |
| CVE-2026-25725 (GHSA-ff64-7w26-62rf) | Claude Code | Before 2.1.2 | CWE-501, CWE-668 | Sandbox escape through configuration injected into `settings.json` | 2026-02-06 |
| CVE-2026-31854 | Cursor | Before 2.0 | CWE-78 | Instructions on a visited website, combined with a bypass of the command allowlist | 2026-03-11 |

## How this maps to OWASP

| OWASP category [R20] | Place in BSA |
|---|---|
| LLM01:2025 Prompt Injection | The cause BSA assumes. The scripted model behaves like a model that was already fooled |
| LLM06:2025 Excessive Agency, which OWASP traces to excessive functionality, permissions or autonomy | What the [control matrix](RESULTS.md#control-matrix) measures: which actions each permission setup still allows |

## Design principle

The repository's safety must not depend on a model obeying a text notice. That failure is what BSA is being built to measure. The notice in `AGENTS.md` is an extra layer. The real protection is meant to be that attacks stay inert outside the arena.
