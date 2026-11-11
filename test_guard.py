"""Offline security checks (Gnani stubbed, no network). Run: python3 test_guard.py"""
import json

from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app import flow, gnani, guard, server, stream

# 1. The case from the browser is untrusted: junk is dropped, a real case survives unchanged.
case, history = {}, ""
for said in ["SBI se 40,000 rupaye gaye UPI se", "30 minute pehle", "9876543210", "KYC update bola", "UTR 412345678901"]:
    case, history = flow.advance(case, history, said)[0]["case"], history + " " + said
    assert {k: flow.clean_case(case)[k] for k in case} == case
evil = flow.clean_case({"amount": "9" * 5000, "txn_id": "1" * 5000, "bank": {"a": 1}, "confirming": "__class__",
                        "fraud_ts": float("nan"), "urged": "yes", "extra": "x" * 9999,
                        "meta": {"bank": {"confirmed": 1, "source_text": "y" * 9999}, "junk": {}, "amount": "no"}})
assert evil["amount"] is None and len(evil["txn_id"]) == 120 and evil["bank"] is None and "extra" not in evil
assert evil["confirming"] is None and evil["fraud_ts"] is None and evil["urged"] is False
assert evil["meta"] == {"bank": {"confirmed": False, "source_text": "y" * 500}}
assert flow.clean_case("not a dict") == flow.clean_case({}) == flow.clean_case(None)

# 2. Sliding-window limiter.
w = guard.Window(2, 10)
assert [w.allow("a", t) for t in (0, 1, 2, 10.5, 11)] == [True, True, False, True, True]
assert w.allow("b", 2)  # one visitor's use doesn't block another

# 3. Other websites can't use the server through a visitor's browser; scripts (no Origin) rely on the limits.
host = {"host": "golden.example"}
assert guard.same_origin(host) and guard.same_origin({**host, "origin": "https://golden.example"})
assert not guard.same_origin({**host, "origin": "https://evil.example"})
assert not guard.same_origin({**host, "origin": "null"})

# 4. HTTP: headers on every reply, no API docs, bad input refused without a 500.
gnani.tts = lambda text, lang="hi": b"RIFF"
web = TestClient(server.app)
page = web.get("/")
csp = page.headers["content-security-policy"]
assert page.status_code == 200 and "default-src 'none'" in csp and "frame-ancestors 'none'" in csp
assert "unsafe-inline" not in csp and "unsafe-eval" not in csp and csp.count("sha256-") == 2
assert page.headers["x-content-type-options"] == "nosniff" and "max-age" in page.headers["strict-transport-security"]
assert " on" not in " ".join(__import__("re").findall(r"<[^>]+>", page.text)).replace(" one", ""), "no inline handlers"
assert all(web.get(p).status_code == 404 for p in ("/docs", "/redoc", "/openapi.json"))
assert web.post("/turn", data={"text": "hi"}, headers={"origin": "https://evil.example"}).status_code == 403
assert web.post("/turn", data={"text": "hi", "case": "{not json"}).status_code == 400
assert web.post("/turn", data={"text": "hi", "case": "[1, 2]"}).status_code == 200
big = web.post("/turn", data={"text": "SBI se 40,000 rupaye gaye " + "x" * 5000, "case": json.dumps({"txn_id": "7" * 9000})})
assert big.status_code == 200 and big.json()["case"]["amount"] == 40000 and len(big.json()["transcript"]) == guard.MAX_TEXT
assert web.post("/turn", files={"audio": ("a.wav", b"\0" * (guard.MAX_AUDIO + 1))}).status_code == 413
assert web.post("/turn", content=b"x" * 3_000_000, headers={"content-type": "text/plain"}).status_code == 413


def boom(*a, **k):
    raise RuntimeError("upstream said: key sk-secret-123 rejected")


gnani.stt = boom
leak = web.post("/turn", files={"audio": ("a.wav", b"\0" * 100)})
assert leak.status_code == 502 and "secret" not in leak.text  # upstream error text never reaches the browser

guard.turns_ip = guard.Window(3, 600)
codes = [web.post("/turn", data={"text": "hi"}).status_code for _ in range(5)]
assert codes == [200, 200, 200, 429, 429], codes

# 5. Live call: foreign origins refused, and no more than MAX_CALLS_IP calls at once per visitor.
try:
    with web.websocket_connect("/ws/call", headers={"origin": "https://evil.example"}):
        raise AssertionError("cross-site WebSocket was accepted")
except WebSocketDisconnect as e:
    assert e.code == 1008


async def hold(ws):
    await ws.receive()


stream.run = hold
open_calls = [web.websocket_connect("/ws/call").__enter__() for _ in range(guard.MAX_CALLS_IP)]
with web.websocket_connect("/ws/call") as extra:
    assert extra.receive_json()["type"] == "error"
for c in open_calls:
    c.close()
print("guard ok")
