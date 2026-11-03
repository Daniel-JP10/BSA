"""The only way out for model traffic, and the only holder of a real API key.

The agent gets a dummy token. This proxy drops it, adds the real key when one
exists, forwards an allowlist of routes and enforces a per-arena request budget.
"""
import http.client
import json
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

UPSTREAM = urllib.parse.urlsplit(os.environ.get("BSA_UPSTREAM", "http://fake-llm:8081"))
KEY_FILE = Path(os.environ.get("BSA_KEY_FILE", "/run/secrets/anthropic_key"))
BUDGET = int(os.environ.get("BSA_MAX_REQUESTS", "200"))
MODELS = {m for m in os.environ.get("BSA_ALLOWED_MODELS", "").split(",") if m}
ROUTES = {("POST", "/v1/messages"), ("POST", "/v1/messages/count_tokens"), ("GET", "/v1/models")}
FORWARD = {"content-type", "anthropic-version", "anthropic-beta", "accept", "x-bsa-script"}
MAX_BODY = 32 * 1024 * 1024
requests_used = 0


def key() -> str | None:
    return KEY_FILE.read_text().strip() if KEY_FILE.exists() else None


def strip_server_tools(payload: dict) -> None:
    """Search runs on the provider's side, outside any network control we have."""
    if "tools" in payload:
        payload["tools"] = [t for t in payload["tools"] if not str(t.get("type", "")).startswith("web_search")]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # never log prompts
        pass

    def refuse(self, status: int) -> None:
        self.send_response(status)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def forward(self, method: str) -> None:
        global requests_used
        route = urllib.parse.urlsplit(self.path).path
        if (method, route) not in ROUTES or requests_used >= BUDGET:
            # Read the body first: closing with unread bytes can reset the connection before the client sees the status.
            self.rfile.read(min(int(self.headers.get("Content-Length") or 0), MAX_BODY))
            return self.refuse(403 if (method, route) not in ROUTES else 429)
        requests_used += 1
        body = None
        if method == "POST":
            length = int(self.headers.get("Content-Length") or 0)
            if length > MAX_BODY:
                return self.refuse(413)
            try:
                payload = json.loads(self.rfile.read(length))
            except ValueError:
                return self.refuse(400)
            if MODELS and payload.get("model") not in MODELS:
                return self.refuse(403)
            strip_server_tools(payload)
            body = json.dumps(payload).encode()
        headers = {k: v for k, v in self.headers.items() if k.lower() in FORWARD}
        secret = key()
        if secret:
            headers["x-api-key"] = secret
        kind = http.client.HTTPSConnection if UPSTREAM.scheme == "https" else http.client.HTTPConnection
        upstream = kind(UPSTREAM.netloc, timeout=300)
        try:
            upstream.request(method, self.path, body=body, headers=headers)
            reply = upstream.getresponse()
            self.send_response(reply.status)
            for name, value in reply.getheaders():
                if name.lower() not in {"transfer-encoding", "connection", "content-length"}:
                    self.send_header(name, value)
            self.send_header("Connection", "close")
            self.end_headers()
            while chunk := reply.read1(65536):
                self.wfile.write(chunk)
                self.wfile.flush()
        except (OSError, ValueError):  # a ValueError can quote a malformed header: keep it out of logs
            self.close_connection = True
        finally:
            upstream.close()

    def do_POST(self):
        self.forward("POST")

    def do_GET(self):
        self.forward("GET")


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
