"""Command line: python -m bsa <command>."""
import argparse
import json
import sys
from pathlib import Path

from . import catalog, runner, stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bsa", description="Benchmark of Safe Attacks")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="check catalog metadata against the safety rules")
    run = sub.add_parser("run", help="run a scenario with the fake agent, inside the arena")
    run.add_argument("scenario")
    run.add_argument("--behaviour", choices=runner.BEHAVIOURS, default="obedient")
    interval = sub.add_parser("wilson", help="print a 95%% interval")
    interval.add_argument("successes", type=int)
    interval.add_argument("runs", type=int)
    args = parser.parse_args(argv)

    if args.command == "validate":
        problems = catalog.validate_all()
        print(json.dumps({"scenarios": len(catalog.load()), "problems": problems}, indent=2))
        return 1 if problems else 0
    if args.command == "wilson":
        low, high = stats.wilson(args.successes, args.runs)
        print(f"{args.successes}/{args.runs}: {low:.1%} to {high:.1%}")
        return 0
    known = {s["id"] for s in catalog.load()}
    if args.scenario not in known:
        print("unknown scenario", file=sys.stderr)
        return 2
    print(json.dumps(runner.run(args.scenario, args.behaviour, Path("/workspace/run"))))
    return 0
