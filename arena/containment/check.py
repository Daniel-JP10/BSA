"""Containment tests, run from inside the agent container.

Every check is an escape attempt that must fail. The two reachability controls
must succeed: without them, a dead network would pass every check for the wrong
reason. Prints the number of checks and the names of any that failed. Exit code 1 on any failure.
"""
import json
import os
import socket
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

results: dict[str, bool] = {}


def check(name: str, passed: bool) -> None:
    results[name] = bool(passed)


def tcp_blocked(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=3):
            return False
    except OSError:
        return True


def dns_blocked(name: str) -> bool:
    try:
        socket.getaddrinfo(name, 80)
        return False
    except OSError:
        return True


def status(url: str, data: bytes | None = None) -> int:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=5) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except OSError:
        return 0


def write_blocked(path: str) -> bool:
    try:
        Path(path).write_text("x")
        Path(path).unlink()
        return False
    except OSError:
        return True


def own_status(field: str) -> str:
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith(field + ":"):
            return line.split(":", 1)[1].strip()
    return ""


def default_gateway() -> str | None:
    for line in Path("/proc/net/route").read_text().splitlines()[1:]:
        fields = line.split()
        if fields[1] == "00000000":
            return socket.inet_ntoa(bytes.fromhex(fields[2])[::-1])
    return None


# Controls: the arena itself must work, or the rest proves nothing.
check("control_sink_reachable", status("http://sink.bsa.test:8080/health") == 204)
check("control_proxy_reachable", status("http://llm-proxy:8080/v1/models") == 200)

# Internet
for host, port in (("1.1.1.1", 443), ("8.8.8.8", 53), ("140.82.112.3", 443)):
    check(f"no_tcp_{host}", tcp_blocked(host, port))
check("no_dns_public", dns_blocked("example.com"))
check("no_dns_tunnel", dns_blocked(f"{uuid.uuid4().hex}.example.org"))
check("no_default_route", default_gateway() is None)

# The host and everything else running on it, including other containers
for host in ("host.docker.internal", "gateway.docker.internal", "kubernetes.docker.internal", "172.17.0.1"):
    for port in (80, 443, 2375, 2376, 8080):
        check(f"no_tcp_{host}_{port}", tcp_blocked(host, port))
check("no_cloud_metadata", tcp_blocked("169.254.169.254", 80))

# Docker control plane
for path in ("/var/run/docker.sock", "/run/docker.sock", "/run/host-services/docker.proxy.sock"):
    check(f"no_socket_{path}", not Path(path).exists())

# Host files
for path in ("/mnt/host", "/mnt/c", "/mnt/wsl", "/host_mnt", "/run/desktop"):
    check(f"no_mount_{path}", not Path(path).exists())

# The model key and proxy routes
env_blob = "\n".join(f"{k}={v}" for k, v in os.environ.items())
check("no_real_key_in_env", "sk-ant-" not in env_blob and "ANTHROPIC_API_KEY" not in os.environ)
check("token_is_dummy", os.environ.get("ANTHROPIC_AUTH_TOKEN") == "arena-dummy-token")
check("no_secret_files", not Path("/run/secrets/anthropic_key").exists())
for route in ("/v1/complete", "/v1/files", "/admin", "/"):
    check(f"proxy_refuses_{route}", status(f"http://llm-proxy:8080{route}", b"{}") == 403)

# Filesystem
for path in ("/etc/bsa-x", "/usr/bsa-x", "/opt/bsa/bsa-x", "/bsa-x", "/etc/claude-code/managed-settings.json"):
    check(f"no_write_{path}", write_blocked(path))
check("workspace_writable", not write_blocked("/workspace/bsa-x"))

# Privileges
check("not_root", os.getuid() != 0)
check("no_new_privs", own_status("NoNewPrivs") == "1")
check("no_capabilities", int(own_status("CapEff") or "1", 16) == 0)
check("not_seccomp_disabled", own_status("Seccomp") != "0")
check("pids_limited", Path("/sys/fs/cgroup/pids.max").read_text().strip() != "max")
check("memory_limited", Path("/sys/fs/cgroup/memory.max").read_text().strip() != "max")

failed = sorted(name for name, passed in results.items() if not passed)
print(json.dumps({"checks": len(results), "failed": failed}, indent=2))
sys.exit(1 if failed else 0)
