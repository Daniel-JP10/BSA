"""Operator entry point for the arena. Run it on the host, never inside a container.

Every Docker call is scoped to the arena's Compose project. This script never
prunes, and it proves it left everything else alone by comparing a snapshot of
foreign containers, networks and volumes before and after each command.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = "bsa-arena"
OURS = "bsa-"
MATRIX = ROOT / "docs" / "MATRIX.json"
DRIFT = ROOT / "docs" / "DRIFT.json"
COMPOSE = ["docker", "compose", "-p", PROJECT, "-f", str(ROOT / "arena" / "compose.yml")]
PY = ["exec", "-T", "agent", "python3"]


def sh(args: list[str], check: bool = True, quiet: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, text=True, encoding="utf-8", errors="replace",
                          capture_output=quiet)


def out(args: list[str]) -> list[str]:
    return sh(args, quiet=True).stdout.split()


def foreign() -> dict:
    """Everything on this machine that does not belong to the arena."""
    ids = out(["docker", "ps", "-aq", "--no-trunc"])
    containers = []
    if ids:
        fmt = '{{.Id}} {{.Name}} {{.State.Status}} {{.State.StartedAt}} {{.RestartCount}} ' \
              '{{index .Config.Labels "com.docker.compose.project"}}'
        lines = sh(["docker", "inspect", "--format", fmt, *ids], quiet=True).stdout.splitlines()
        containers = sorted(line for line in lines if not line.rsplit(" ", 1)[-1].startswith(OURS))
    networks = [n for n in out(["docker", "network", "ls", "--format", "{{.ID}}:{{.Name}}"])
                if not n.split(":")[1].startswith(OURS)]
    volumes = [v for v in out(["docker", "volume", "ls", "--format", "{{.Name}}"]) if not v.startswith(OURS)]
    return {"containers": containers, "networks": sorted(networks), "volumes": sorted(volumes)}


def inspect_arena() -> list[str]:
    """Static checks from outside. Returns problems found in the running arena."""
    problems = []
    ids = sh([*COMPOSE, "ps", "-q"], quiet=True).stdout.split()
    if not ids:
        return ["arena is not running"]
    for item in json.loads(sh(["docker", "inspect", *ids], quiet=True).stdout):
        host, name = item["HostConfig"], item["Name"].strip("/")
        checks = {
            "privileged": not host["Privileged"],
            "binds": not host.get("Binds"),
            "mounts": all(m["Type"] == "tmpfs" for m in item["Mounts"]),
            "ports": not host.get("PortBindings"),
            "caps": host.get("CapDrop") == ["ALL"] and not host.get("CapAdd"),
            "read_only": host["ReadonlyRootfs"],
            "pid_mode": host.get("PidMode") == "",
            "restart": host["RestartPolicy"]["Name"] == "no",
            "memory": host["Memory"] > 0,
            "pids": (host.get("PidsLimit") or 0) > 0,
            "networks": all("arena" in n for n in item["NetworkSettings"]["Networks"]),
        }
        problems += [f"{name}:{check}" for check, passed in checks.items() if not passed]
    for network in out(["docker", "network", "ls", "--filter", f"name={PROJECT}", "--format", "{{.Name}}"]):
        if sh(["docker", "network", "inspect", network, "--format", "{{.Internal}}"], quiet=True).stdout.strip() != "true":
            problems.append(f"{network}:not-internal")
    return problems


def up() -> None:
    sh([*COMPOSE, "build", "--quiet"])
    sh([*COMPOSE, "up", "-d", "--wait", "--quiet-pull"])


def down() -> None:
    sh([*COMPOSE, "down", "-v", "--remove-orphans", "-t", "2"], quiet=True)


def smoke() -> int:
    """The fake agent must produce each outcome the observers can see."""
    expected = {"obedient": "COMPROMISED", "ignores": "IGNORED", "refuses": "DETECTED"}
    failures = 0
    for behaviour, outcome in expected.items():
        done = sh([*COMPOSE, *PY, "-m", "bsa", "run", "BSA-SMOKE-0001", "--behaviour", behaviour], quiet=True)
        got = json.loads(done.stdout)["outcome"]
        print(f"{behaviour}: {got}")
        failures += got != outcome
    return failures


def open_network() -> int:
    """Show the network checks can fail: a copy with the network opened must reach the internet."""
    base = ["docker", "compose", "-p", "bsa-open-network", "-f", str(ROOT / "arena" / "compose.yml"),
            "-f", str(ROOT / "arena" / "compose.open-network.yml")]
    try:
        sh([*base, "up", "-d", "--wait", "--quiet-pull"], quiet=True)
        return sh([*base, *PY, "/opt/bsa/containment/open_network.py"], check=False).returncode
    finally:
        sh([*base, "down", "-v", "--remove-orphans", "-t", "2"], quiet=True)


def matrix(repetitions: int) -> int:
    """Every risky action against every permission setup, compared with the recorded table."""
    done = sh([*COMPOSE, *PY, "/opt/bsa/containment/matrix.py", str(repetitions)], check=False, quiet=True)
    if not done.stdout.strip():
        print(done.stderr[-800:])
        return 1
    result = json.loads(done.stdout)
    print(json.dumps(result, indent=1))
    if "--record" in sys.argv:
        MATRIX.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8", newline="\n")
        return done.returncode
    return int(done.returncode != 0 or result["ran"] != json.loads(MATRIX.read_text(encoding="utf-8"))["ran"])


def drift(versions: list[str]) -> int:
    """The same contracts on several agent versions. Observes, and never compares."""
    results = {}
    for version in versions:
        os.environ["BSA_AGENT_VERSION"] = version
        try:
            up()
            done = sh([*COMPOSE, *PY, "/opt/bsa/containment/contracts.py", "--observe"], quiet=True)
            results[version] = json.loads(done.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as error:
            results[version] = {"agent": version, "error": type(error).__name__}  # a version may lack something we use
        finally:
            down()
            sh(["docker", "image", "rm", f"bsa/agent:{version}"], check=False, quiet=True)
    os.environ.pop("BSA_AGENT_VERSION", None)
    print(json.dumps(results, indent=1))
    if "--record" in sys.argv:
        DRIFT.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8", newline="\n")
    return 0


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    commands = {"all", "up", "down", "contain", "smoke", "contract", "open-network", "matrix", "drift"}
    if command not in commands:
        print(__doc__ + "\nCommands: " + ", ".join(sorted(commands)))
        return 2
    if not str(ROOT).isascii():
        print("The arena build failed from folder paths with non-ASCII characters. Move the clone first.")
        return 2
    if command in {"matrix", "drift"}:
        os.environ["BSA_MAX_REQUESTS"] = "6000"  # hundreds of agent runs, all answered by the scripted model
    before = foreign()
    failures = 0
    try:
        if command == "up":
            up()
        elif command == "down":
            down()
        elif command == "open-network":
            sh([*COMPOSE, "build", "--quiet"])
            failures += open_network()
        elif command == "drift":
            failures += drift([v for v in sys.argv[2:] if not v.startswith("--")])
        else:
            up()
            problems = inspect_arena()
            print("outside inspection:", problems or "clean")
            failures += len(problems)
            if not problems and command in {"all", "contain"}:
                failures += sh([*COMPOSE, *PY, "/opt/bsa/containment/check.py"], check=False).returncode
            if not failures and command in {"all", "smoke"}:
                failures += smoke()
            if not failures and command in {"all", "contract"}:
                failures += sh([*COMPOSE, *PY, "/opt/bsa/containment/contracts.py", *sys.argv[2:]],
                               check=False).returncode
            if not failures and command == "matrix":
                numbers = [a for a in sys.argv[2:] if a.isdigit()]
                failures += matrix(int(numbers[0]) if numbers else 3)
    finally:
        if command not in {"up", "down", "open-network", "drift"}:
            down()
    after = foreign()
    if before != after:
        print("FOREIGN RESOURCES CHANGED:", [k for k in before if before[k] != after[k]])  # names stay private
        return 3
    print("foreign resources: unchanged")
    print("failures:", failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
