"""Manage the development container from the host.

  up      build and start it
  seed    copy the publishable files into its volume
  shell   open a shell inside it
  down    stop it and keep the volumes
  purge   stop it and delete its volumes
"""
import io
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPOSE = ["docker", "compose", "-p", "bsa-dev", "-f", str(ROOT / "dev" / "compose.yml")]


def publishable() -> list[str]:
    """Exactly what git would publish: tracked or untracked, minus everything ignored."""
    args = ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard"]
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.splitlines()


def seed() -> None:
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w") as tar:
        for name in publishable():
            tar.add(ROOT / name, arcname=name)
    subprocess.run([*COMPOSE, "exec", "-T", "dev", "tar", "-xf", "-", "-C", "/workspace"],
                   input=archive.getvalue(), check=True)
    # An empty local repository, so tools that ask git what is publishable work here too.
    subprocess.run([*COMPOSE, "exec", "-T", "dev", "git", "-C", "/workspace", "init", "-q"], check=True)


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "up":
        return subprocess.run([*COMPOSE, "up", "-d", "--build", "--wait"]).returncode
    if command == "seed":
        seed()
        return 0
    if command == "shell":
        return subprocess.run([*COMPOSE, "exec", "dev", "bash"]).returncode
    if command == "down":
        return subprocess.run([*COMPOSE, "down", "-t", "2"]).returncode
    if command == "purge":
        return subprocess.run([*COMPOSE, "down", "-v", "-t", "2"]).returncode
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
