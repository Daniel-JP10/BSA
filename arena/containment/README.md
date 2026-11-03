# arena/containment

[Español](README.es.md)

## What this is

The test programs that run inside the arena.

- `check.py` tries to escape: reaching the internet, host addresses, the Docker API, host files and the real key, or writing to system paths. Each attempt must fail. Two connectivity controls must succeed, so a dead network cannot pass by accident.
- `contracts.py` measures how the real agent binary behaves against a scripted model: does a permission rule or a hook actually stop a command? The only evidence is whether the side effect happened, and the run fails if a result differs from the recorded one. It also records which commands run without approval, and whether a `deny` hook stops them.
- `matrix.py` crosses 16 harmless actions with 7 permission setups and records which ones produced their effect. Its Bypass column is a control: if an action does not run there, the test itself is broken.
- `open_network.py` runs in a copy of the arena with its network opened, and passes only if the internet is reachable.

## Warning

A green result covers these checks on this setup, not every possible escape. If a check fails, stop: no attacks run until it is understood. Contract results describe one agent version and may change with the next.

## For humans

```sh
python scripts/arena.py contain
python scripts/arena.py contract
python scripts/arena.py contract <case> <case>
python scripts/arena.py matrix
python scripts/arena.py drift <version> <version>
```

Write a new containment check as an attempt that must fail. If it could pass for the wrong reason, add a control proving the path was usable. To add a contract, add an entry to `CASES` in `contracts.py`, and to `RAN` if the command is expected to run. To add a matrix action, add it to `ACTIONS` in [`fake_llm.py`](../services/fake_llm.py) and to `READS` or `EFFECTS` in `matrix.py`. To add a setup, add it to `PROFILES`. Then record the new table with `python scripts/arena.py matrix 3 --record`.

## For AI agents

Report a failing check instead of weakening, skipping or deleting it. The escape attempts here are tests, and they run only inside the arena.
