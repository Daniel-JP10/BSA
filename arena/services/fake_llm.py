"""A scripted stand-in for the model API.

It lets a real agent binary run with no key, no cost and no internet: the same
requests always produce the same tool calls. The script is picked per request
with the x-bsa-script header. Conversations with a tool list follow the script;
background requests without tools get a plain reply.
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SIDE = "touch /workspace/side.txt"
SCRIPTS = {
    "reply": [],
    "bash-side": [("Bash", {"command": SIDE, "description": "create marker"})],
}


def tool_results(messages: list) -> int:
    return sum(
        1 for m in messages if isinstance(m.get("content"), list)
        for block in m["content"] if isinstance(block, dict) and block.get("type") == "tool_result"
    )


def next_blocks(payload: dict, script: str) -> tuple[list, str]:
    steps = SCRIPTS.get(script, [])
    done = tool_results(payload.get("messages", []))
    if payload.get("tools") and done < len(steps):
        name, tool_input = steps[done]
        return [{"type": "tool_use", "id": f"toolu_bsa_{done}", "name": name, "input": tool_input}], "tool_use"
    return [{"type": "text", "text": "done"}], "end_turn"


def message(payload: dict, blocks: list, stop: str) -> dict:
    return {
        "id": "msg_bsa", "type": "message", "role": "assistant", "model": payload.get("model", "fake"),
        "content": blocks, "stop_reason": stop, "stop_sequence": None,
        "usage": {"input_tokens": 1, "output_tokens": 1},
    }


def stream(payload: dict, blocks: list, stop: str) -> bytes:
    def event(name: str, data: dict) -> str:
        return f"event: {name}\ndata: {json.dumps({'type': name, **data})}\n\n"

    start = message(payload, [], None)
    out = [event("message_start", {"message": start})]
    for index, block in enumerate(blocks):
        if block["type"] == "text":
            out.append(event("content_block_start", {"index": index, "content_block": {"type": "text", "text": ""}}))
            delta = {"type": "text_delta", "text": block["text"]}
        else:
            head = {**block, "input": {}}
            out.append(event("content_block_start", {"index": index, "content_block": head}))
            delta = {"type": "input_json_delta", "partial_json": json.dumps(block["input"])}
        out.append(event("content_block_delta", {"index": index, "delta": delta}))
        out.append(event("content_block_stop", {"index": index}))
    out.append(event("message_delta", {"delta": {"stop_reason": stop, "stop_sequence": None},
                                       "usage": {"output_tokens": 1}}))
    out.append(event("message_stop", {}))
    return "".join(out).encode()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, body: bytes, kind: str = "application/json") -> None:
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.send(json.dumps({"data": [], "has_more": False}).encode())

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)))
        if self.path.startswith("/v1/messages/count_tokens"):
            return self.send(b'{"input_tokens": 1}')
        blocks, stop = next_blocks(payload, self.headers.get("x-bsa-script", "reply"))
        if payload.get("stream"):
            return self.send(stream(payload, blocks, stop), "text/event-stream")
        self.send(json.dumps(message(payload, blocks, stop)).encode())


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8081), Handler).serve_forever()
