"""Runs in a deliberately opened arena. Exit 0 only if the internet IS reachable."""
import socket
import sys

reached = 0
for host, port in (("1.1.1.1", 443), ("8.8.8.8", 53)):
    try:
        socket.create_connection((host, port), timeout=5).close()
        reached += 1
    except OSError:
        pass
print(f"opened network reached {reached} of 2 public addresses")
sys.exit(0 if reached == 2 else 1)
