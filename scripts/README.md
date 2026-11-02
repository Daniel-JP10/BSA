# scripts

[Español](README.es.md)

## What this is

Commands that run on the host.

| Script | Role |
|---|---|
| `arena.py` | Builds, verifies, runs and removes the arena, and checks that containers, networks and volumes from other projects did not change |
| `dev.py` | Manages the development container |
| `exposure_audit.py` | Scans what Git would publish and the full commit history for secrets, personal data, hidden characters, image metadata and forbidden files |
| `analyze_published.py` | Recalculates the published IssueTrojanBench results inside a container with no network. See [Published data](../docs/PUBLISHED_DATA.md) |

## Warning

- Run these on the host: no container in this project has access to Docker.
- They never run `docker system prune` or any other command that changes resources outside this project. Keep it that way.
- **Run the audit before every push.** Git history is permanent once pushed, so a secret removed later stays exposed.
- The audit is run by hand and cannot find everything. It complements a person's review.

## For humans

```sh
python scripts/exposure_audit.py
```

To search for your own name, username or email without publishing them, list them in `.bsa-audit-terms`, one per line. Git ignores that file, and the audit warns if it found no terms to load. Results show rule and location only, never the matched text.

To recalculate the published IssueTrojanBench results, run `python scripts/analyze_published.py issuetrojanbench.zip`. The script's header explains what it checks.

## For AI agents

Run the audit and show its result before saying it passed. Do not add broad Docker commands to these scripts.
