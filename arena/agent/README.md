# arena/agent

[Español](README.es.md)

## What this is

The image the agent runs in. It carries Claude Code pinned to an exact version, plus `curl`, `git` and Python on purpose: containment has to come from the environment, so the tools stay available.

| File | Role |
|---|---|
| `Dockerfile` | The image, with its base pinned by digest |
| `managed-settings.json` | Managed-level hook used by the contract tests |
| `deny_hook.py` | Test hook that acts only when a test creates its flag file |

## Warning

This image is a test subject, so keep it away from everyday work and real credentials. The managed settings file exists for the contract tests and protects nothing.

## For humans

`python scripts/arena.py up` builds the image. To look at another agent version without changing anything, run `python scripts/arena.py drift <version>`. To move the pin, change the default in `Dockerfile` and `compose.yml`, rerun `python scripts/arena.py all`, and record the matrix again. Results apply to one version only, so a new version may need new recorded values in `contracts.py`.

## For AI agents

Keep the version pin in place, and do not copy these settings or this hook into a real environment.
