# tests

[Español](README.es.md)

## What this is

Unit tests with no Docker, no key and no network. `test_core.py` covers statistics, outcomes, the safety validator, the result filter, the proxy's search-tool filter, the scripted model and the audit. `test_docs.py` checks that every folder documents itself in both languages.

## Warning

These tests do not exercise containment. Run `python scripts/arena.py all` for that, and see the limitations for what it does not cover. They also need a Git clone, because `test_docs.py` asks Git for the file list.

## For humans

```sh
python -m unittest discover -s tests
```

## For AI agents

If a safety test fails, report it. Changing the expected result to make it pass is not a fix.
