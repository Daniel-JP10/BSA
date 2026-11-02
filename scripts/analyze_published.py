"""Recalculate the published IssueTrojanBench results inside a container with no network.

  python scripts/analyze_published.py issuetrojanbench.zip

The archive is checked against the MD5 Zenodo lists for version 1.0.0 and refused if it differs,
unless --any-version is given. It is copied into a throwaway container (no network, read-only root,
no capabilities, 512 MB) and read there, never extracted: nothing from it is executed. The
container is removed at the end, and only the aggregate numbers come back.
"""
import argparse
import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from bsa.published import EXPECTED_MD5, render  # noqa: E402

IMAGE = "python@sha256:e6dae589c1c05976188fd3bd019afd091445fc533ed2ea29001beddc7368a9c8"
NAME = "bsa-analysis"
MAX_ARCHIVE = 50_000_000


def docker(*args: str, data: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["docker", *args], input=data, capture_output=True, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("archive", type=Path)
    parser.add_argument("--json", action="store_true", help="print the raw numbers instead of a table")
    parser.add_argument("--any-version", action="store_true", help="analyze an archive whose MD5 differs")
    args = parser.parse_args()

    data = args.archive.read_bytes()
    if len(data) > MAX_ARCHIVE:
        print("archive is larger than expected")
        return 2
    md5 = hashlib.md5(data).hexdigest()
    print(f"archive MD5 {md5}", "matches" if md5 == EXPECTED_MD5 else f"DIFFERS from the listed {EXPECTED_MD5}")
    if md5 != EXPECTED_MD5 and not args.any_version:
        print("refusing to analyze it; pass --any-version to override")
        return 2

    bundle = io.BytesIO()
    with tarfile.open(fileobj=bundle, mode="w") as tar:
        for path in sorted((ROOT / "bsa").glob("*.py")):
            tar.add(path, arcname=f"bsa/{path.name}")
        info = tarfile.TarInfo("issuetrojanbench.zip")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))

    subprocess.run(["docker", "rm", "-f", NAME], capture_output=True)
    try:
        docker("run", "-d", "--name", NAME, "--network", "none", "--read-only", "--cap-drop", "ALL",
               "--security-opt", "no-new-privileges", "--user", "10001:10001", "--pids-limit", "64",
               "--memory", "512m", "--cpus", "1", "--tmpfs", "/work:size=96m,mode=1777", "-e", "PYTHONPATH=/work",
               "-e", "PYTHONDONTWRITEBYTECODE=1", "-w", "/work", IMAGE, "sleep", "300")
        docker("exec", "-i", NAME, "tar", "-xf", "-", "-C", "/work", data=bundle.getvalue())
        done = docker("exec", NAME, "python3", "-m", "bsa.published", "/work/issuetrojanbench.zip")
    except subprocess.CalledProcessError as error:
        print("analysis failed:", error.stderr.decode(errors="replace")[-600:])
        return 1
    finally:
        subprocess.run(["docker", "rm", "-f", NAME], capture_output=True)

    summary = json.loads(done.stdout)
    print(json.dumps(summary, indent=1) if args.json else render(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
