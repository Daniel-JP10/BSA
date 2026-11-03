"""Recalculate the per-run results of IssueTrojanBench from its published spreadsheets.

The data is CC BY 4.0 (Zenodo, DOI 10.5281/zenodo.22983053, version 1.0.0). This module only reads
the spreadsheets inside the archive: it never extracts files and never runs anything from it.
Run it through scripts/analyze_published.py, which does it in a container without network access.
"""
import collections
import io
import json
import sys
import zipfile

from .stats import clustered_mean, wilson
from .xlsx import read_book

EXPECTED_MD5 = "3e335d29585764f054029b7f43b4f4cb"  # listed on the Zenodo page for version 1.0.0
COLUMNS = ("Issue_ID", "Attack_Category", "Agent_Framework", "Model", "Delivery_Vector", "Perturbation",
           "EEM_Score", "Rejection_Attribution")
SUFFIX = "Results_final.xlsx"
MAX_MEMBER = 20_000_000


def read_runs(archive) -> list[dict]:
    """Every per-run row of the two results workbooks. Raises ValueError if the layout is not the expected one."""
    rows = []
    with zipfile.ZipFile(archive) as z:
        members = sorted(n for n in z.namelist() if n.endswith(SUFFIX))
        if not members:
            raise ValueError(f"no *{SUFFIX} workbook in the archive")
        for name in members:
            if z.getinfo(name).file_size > MAX_MEMBER:
                raise ValueError(f"{name} is too large")
            for sheet, table in read_book(io.BytesIO(z.read(name))).items():
                if sheet == "Metrics":
                    continue
                if tuple(table[0][:len(COLUMNS)]) != COLUMNS:
                    raise ValueError(f"unexpected columns in sheet {sheet!r}")
                for values in table[1:]:
                    row = dict(zip(COLUMNS, (list(values) + [None] * len(COLUMNS))[:len(COLUMNS)]))
                    if row["EEM_Score"] not in (0, 1):
                        raise ValueError(f"EEM_Score is not 0 or 1 in sheet {sheet!r}")
                    rows.append(row)
    return rows


def _tally(rows, key) -> dict:
    groups = collections.defaultdict(lambda: [0, 0])
    for row in rows:
        groups[key(row)][0] += row["EEM_Score"]
        groups[key(row)][1] += 1
    return {k: {"successes": s, "runs": n} for k, (s, n) in sorted(groups.items())}


def summarize(rows: list[dict]) -> dict:
    keys = collections.Counter(tuple(r[c] for c in COLUMNS[:6]) for r in rows)
    combos = collections.defaultdict(list)
    for r in rows:
        combos[(r["Issue_ID"], r["Attack_Category"], r["Agent_Framework"], r["Model"])].append(r["EEM_Score"])

    def shape(scores):
        return "succeeds in every run" if all(scores) else "fails in every run" if not any(scores) else "mixed"

    mixed_vectors = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        if shape(combos[(r["Issue_ID"], r["Attack_Category"], r["Agent_Framework"], r["Model"])]) == "mixed":
            mixed_vectors[r["Delivery_Vector"]][0] += r["EEM_Score"]
            mixed_vectors[r["Delivery_Vector"]][1] += 1

    outcomes = collections.defaultdict(dict)
    for r in rows:
        outcomes[(r["Issue_ID"], r["Attack_Category"], r["Delivery_Vector"], r["Perturbation"], r["Model"])][
            r["Agent_Framework"]] = r["EEM_Score"]
    across = {}
    for model in sorted({r["Model"] for r in rows}):
        paired = [v for k, v in outcomes.items() if k[4] == model and len(v) > 1]
        across[model] = {"products": sorted({a for v in paired for a in v}), "paired_runs": len(paired),
                         "same_outcome": sum(len(set(v.values())) == 1 for v in paired)}

    claude = [r for r in rows if r["Agent_Framework"] == "Claude Code"]
    claude_combos = {k: v for k, v in combos.items() if k[2] == "Claude Code"}
    any_success = sum(1 for v in claude_combos.values() if any(v))
    wins = sum(r["EEM_Score"] for r in claude)
    refusals = collections.Counter((r["Model"], r["Rejection_Attribution"]) for r in rows if r["EEM_Score"] == 0)
    return {
        "runs": len(rows),
        "distinct_configurations": len(keys),
        "repeated_configurations": sum(1 for v in keys.values() if v > 1),
        "successes": sum(r["EEM_Score"] for r in rows),
        "by_agent_and_model": _tally(rows, lambda r: f"{r['Agent_Framework']} + {r['Model']}"),
        "by_attack_category": _tally(rows, lambda r: r["Attack_Category"]),
        "by_delivery_vector": _tally(rows, lambda r: r["Delivery_Vector"]),
        "combinations": {
            "total": len(combos),
            "runs_per_combination": dict(collections.Counter(str(len(v)) for v in combos.values())),
            "shape": dict(collections.Counter(shape(v) for v in combos.values())),
        },
        "mixed_combinations_by_vector": {k: {"successes": s, "runs": n} for k, (s, n) in sorted(mixed_vectors.items())},
        "same_model_across_products": across,
        "claude_code": {
            "by_attack_category": _tally(claude, lambda r: r["Attack_Category"]),
            "by_delivery_vector": _tally(claude, lambda r: r["Delivery_Vector"]),
            "combinations": len(claude_combos),
            "combinations_with_a_success": any_success,
            "interval_over_combinations": [round(x, 4) for x in wilson(any_success, len(claude_combos))] if claude_combos else None,
            "interval_over_runs_if_independent": [round(x, 4) for x in wilson(wins, len(claude))] if claude else None,
            "clustered_over_runs": {k: round(v, 4) for k, v in clustered_mean(list(claude_combos.values())).items()} if claude else None,
        },
        "clustered_by_agent_and_model": {f"{a} + {m}": {k: round(v, 4) for k, v in clustered_mean(
            [s for key, s in combos.items() if key[2:] == (a, m)]).items()}
            for a, m in sorted({key[2:] for key in combos})},
        "rejections_by_model": {f"{m} / {a}": n for (m, a), n in sorted(refusals.items(), key=str)},
    }


def render(summary: dict) -> str:
    """A readable version of summarize(), for people."""
    out = [f"runs: {summary['runs']}, distinct configurations: {summary['distinct_configurations']}, "
           f"repeated: {summary['repeated_configurations']}, successes: {summary['successes']} "
           f"({summary['successes'] / summary['runs']:.1%})"]

    def block(title, table):
        out.append(f"\n{title}")
        out.extend(f"  {k:36} {v['successes']:5} / {v['runs']:<5} {v['successes'] / v['runs']:6.1%}" for k, v in table.items())

    block("by agent and model", summary["by_agent_and_model"])
    block("by attack category", summary["by_attack_category"])
    block("by delivery vector", summary["by_delivery_vector"])
    c = summary["combinations"]
    out.append(f"\ncombinations: {c['total']}, runs per combination {c['runs_per_combination']}, shape {c['shape']}")
    block("inside mixed combinations, by delivery vector", summary["mixed_combinations_by_vector"])
    out.append("\nsame model, different products")
    for model, d in summary["same_model_across_products"].items():
        out.append(f"  {model:16} {', '.join(d['products'])}: {d['same_outcome']} of {d['paired_runs']} paired runs gave the same outcome")
    cc = summary["claude_code"]
    block("Claude Code, by attack category", cc["by_attack_category"])
    block("Claude Code, by delivery vector", cc["by_delivery_vector"])
    out.append(f"\nClaude Code combinations with a success: {cc['combinations_with_a_success']} of {cc['combinations']}, "
               f"interval over combinations {cc['interval_over_combinations']}; "
               f"interval over runs, if they were independent {cc['interval_over_runs_if_independent']}")
    out.append("\ncluster-adjusted rates, one cluster per combination")
    out.extend(f"  {k:36} {v['mean']:6.1%}  se {v['se']:.1%}  interval {v['low']:.1%} to {v['high']:.1%}  ({v['clusters']} clusters)"
               for k, v in summary["clustered_by_agent_and_model"].items())
    out.append("\nrejected runs by model and label")
    out.extend(f"  {k}: {v}" for k, v in summary["rejections_by_model"].items())
    return "\n".join(out)


if __name__ == "__main__":
    json.dump(summarize(read_runs(sys.argv[1])), sys.stdout, indent=1)
