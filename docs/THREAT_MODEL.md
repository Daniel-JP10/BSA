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

| Threat | Who is at risk | Main defence | Status |
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

## Design principle

The repository's safety must not depend on a model obeying a text notice. That failure is what BSA is being built to measure. The notice in `AGENTS.md` is an extra layer. The real protection is meant to be that attacks stay inert outside the arena.
