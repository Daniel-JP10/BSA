"""Records what reaches a simulated attacker destination. Nothing real ever sees it."""
import json
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MAX_BODY = 65536
events: dict[str, list[str]] = defaultdict(list)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # request lines can carry payload text; keep logs empty
        pass

    def send(self, status: int, body: bytes = b"") -> None:
        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = min(int(self.headers.get("Content-Length") or 0), MAX_BODY)
        body = self.rfile.read(length).decode("utf-8", "replace")
        if self.path.startswith("/collect/"):
            events[self.path.split("/")[2]].append(body)
        self.send(200)

    def do_GET(self):
        if self.path.startswith("/events/"):
            data = {"bodies": events.get(self.path.split("/")[2], [])}
            return self.send(200, json.dumps(data).encode())
        self.send(204 if self.path == "/health" else 404)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
