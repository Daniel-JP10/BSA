# Contributing

[Español](CONTRIBUTING.es.md)

The attack catalog is not open for contributions yet. Fixes to the arena, the runner and the documentation are welcome.

## Rules for every scenario

| Rule | Requirement |
|---|---|
| R1 | No real credentials. Canaries are generated for each run |
| R2 | No real domains. Destinations end in `.test` and resolve only inside the arena |
| R3 | Payloads use placeholders resolved only by the runner (not implemented yet) |
| R4 | No destructive actions. Destruction is modeled by touching a decoy |
| R5 | No malware, no exploitation of real vulnerabilities, no persistence outside the container |
| R6 | No real targets: no people, organizations or services |
| R7 | The validator must pass, and a person reviews every payload |

## Before opening a pull request

```sh
python -m unittest discover -s tests
python -m bsa validate
python scripts/arena.py all
python scripts/exposure_audit.py
```

Documentation is bilingual. Every folder has `README.md` and `README.es.md`, and a change to one needs the same change to the other. `tests/test_docs.py` checks the required sections.

Reviewing scenario metadata with an agent is allowed only inside the development container, treating it as data. Attack packs never enter that container.
