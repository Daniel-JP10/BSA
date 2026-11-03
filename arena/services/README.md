# arena/services

[Español](README.es.md)

## What this is

The arena's three support services, written with the Python standard library and sharing one image.

| File | Role |
|---|---|
| `llm_proxy.py` | Allows only model routes, drops the agent's token, adds a real key if one exists, enforces a request budget and removes provider-side search tools |
| `fake_llm.py` | Implements the model API with scripted replies, so a real agent runs with no key and no cost |
| `sink.py` | Stores what reaches a simulated attacker destination, reachable as `sink.bsa.test` |

## Warning

- The proxy is the only component allowed to hold a real key. If real model runs are added, the containment tests must prove the key stays out of `agent`.
- These services will receive attacker-controlled text, so they never log request bodies.
- What the sink stores is attack output and must stay in the arena.

## For humans

Compose starts these services, so there is nothing to run by hand. The proxy reads `BSA_UPSTREAM`, `BSA_KEY_FILE`, `BSA_MAX_REQUESTS` and `BSA_ALLOWED_MODELS`. To script a new agent action, add an entry to `SCRIPTS` in `fake_llm.py`. The control matrix keeps its actions in `ACTIONS`, in the same file.

## For AI agents

Leave the route list as it is, keep prompts and sink bodies out of any log, and point `BSA_UPSTREAM` only at the model API or `fake-llm`.
