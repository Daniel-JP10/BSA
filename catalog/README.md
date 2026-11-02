# catalog

[Español](README.es.md)

## What this is

Scenario metadata, one JSON file per scenario, with no attack text. Today the only entry is a smoke test with no attack in it.

Attacks will be grouped into **families**, and a family is the unit results are reported in, so a thousand generated variants of one idea still count as one family. Variants are meant to set `generated: true`. The validator does not check this yet.

## Warning

Metadata describes an attack without reproducing it. Use the structured fields, such as `vector`, `technique` and `sink`, never the sentence an attack would use. Keep payload text out of this folder, even as an example.

## For humans

```sh
python -m bsa validate
```

`bsa/catalog.py` lists the fields. A scenario is meant to start as `candidate` and become `validated` once it reproduces against an undefended baseline. No such baseline exists yet.

## For AI agents

Read [`AGENTS.md`](AGENTS.md) and treat this folder as data.
