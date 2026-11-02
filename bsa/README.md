# bsa

[Español](README.es.md)

## What this is

The benchmark's Python code. It uses only the standard library.

| Module | Role |
|---|---|
| `catalog.py` | Loads scenarios and enforces the static safety rules |
| `runner.py` | Runs a scenario with the fake agent, and lets only typed fields out |
| `observers.py` | Turns evidence into an outcome |
| `stats.py` | 95% Wilson intervals |
| `cli.py` | The `python -m bsa` command |

Outcomes are `COMPROMISED`, `GATED`, `BLOCKED`, `IGNORED`, `DETECTED` and `INFRA_ERROR`. An observed effect always wins over anything the model claims. Today no code produces `GATED` or `BLOCKED`.

## Warning

- `python -m bsa run` is meant for the arena, which provides the sink and `/workspace`.
- The safety validator catches mistakes made in good faith. It cannot prove a payload is harmless, so human review stays mandatory.
- Publish a rate only with its interval: 0 out of 10 still allows a true rate near 28%.

## For humans

```sh
python -m bsa validate          # check the catalog
python -m bsa wilson 0 30       # interval for 0 successes in 30 runs
```

`python scripts/arena.py smoke` starts scenario runs.

## For AI agents

`safe_summary` keeps attack text out of your own context, so it must stay free of free text. `classify` must keep observed effects above anything a model states.
