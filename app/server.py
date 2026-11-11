"""Golden Hour API. Run: python3 -m uvicorn app.server:app --reload  -> http://127.0.0.1:8000

WS /ws/call is the live call (streaming STT/TTS, see app/stream.py).
POST /turn is the fallback: one recorded clip or typed line per request; the browser keeps the case.
Both are public and unauthenticated, so app/guard.py limits them and everything from the browser is
treated as untrusted (flow.clean_case, size caps).
"""
import base64
import hashlib
import json
import re
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile, WebSocket
from fastapi.responses import JSONResponse, Response

from app import flow, gnani, guard, stream

app = FastAPI(title="Golden Hour", docs_url=None, redoc_url=None, openapi_url=None)
PAGE = (Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8")


def _hashes(tag: str) -> str:
    """CSP hashes of the page's inline <script>/<style>, so only the code shipped in index.html can run."""
    return " ".join("'sha256-" + base64.b64encode(hashlib.sha256(body.encode()).digest()).decode() + "'"
                    for body in re.findall(rf"<{tag}>(.*?)</{tag}>", PAGE, re.S))


HEADERS = {
    # blob: is the mic AudioWorklet; data:/blob: media is the fallback reply audio. No third-party hosts at all.
    "Content-Security-Policy": f"default-src 'none'; script-src {_hashes('script')} blob:; style-src {_hashes('style')}; "
                               "connect-src 'self'; media-src data: blob:; img-src 'self' data:; "
                               "base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
    "Strict-Transport-Security": "max-age=31536000",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "microphone=(self), camera=(), geolocation=(), payment=()",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cache-Control": "no-store",  # replies carry the caller's case; nothing may be cached
}


def _refuse(request: Request) -> Optional[JSONResponse]:
    if request.method != "POST":
        return None
    if not guard.same_origin(request.headers):
        return JSONResponse({"detail": "Cross-site requests are not allowed."}, 403)
    size = request.headers.get("content-length", "")
    if not size.isdigit():
        return JSONResponse({"detail": "Content-Length required."}, 411)
    if int(size) > guard.MAX_AUDIO + 2 * guard.MAX_CASE:
        return JSONResponse({"detail": "Recording too long, please keep it under 25 seconds."}, 413)
    if not guard.admit_turn(guard.client_ip(request)):
        return JSONResponse({"detail": "Too many requests. Please wait a few minutes, or call 1930 directly."}, 429)
    return None


@app.middleware("http")
async def harden(request: Request, call_next):
    response = _refuse(request) or await call_next(request)
    response.headers.update(HEADERS)
    return response


@app.get("/")
def index():
    return Response(PAGE, media_type="text/html")


@app.websocket("/ws/call")
async def ws_call(ws: WebSocket):
    if not guard.same_origin(ws.headers):
        return await ws.close(1008)
    ip = guard.client_ip(ws)
    await ws.accept()
    if not guard.admit_call(ip):
        await ws.send_json({"type": "error", "message": "Too many calls right now. Please try again in a few "
                                                        "minutes, or call 1930 directly."})
        return await ws.close(1013)
    try:
        await stream.run(ws)
    finally:
        guard.release_call(ip)


@app.post("/turn")
def turn(case: str = Form("{}"), history: str = Form(""), text: str = Form(""), lang: str = Form(""),
         audio: Optional[UploadFile] = File(None)):
    lang = lang if lang in flow.QUESTIONS else ""
    history = history[-guard.MAX_HISTORY:]
    try:
        case = flow.clean_case(json.loads(case[:guard.MAX_CASE] or "{}"))
    except ValueError:
        raise HTTPException(400, "Bad case data, please reload the page.")
    if audio is not None:
        clip = audio.file.read(guard.MAX_AUDIO + 1)
        if len(clip) > guard.MAX_AUDIO:
            raise HTTPException(413, "Recording too long, please keep it under 25 seconds.")
        try:
            heard = gnani.stt(clip, "audio.wav", history, lang)
            said, hint = heard["transcript"], heard.get("detected_language_code")
        except Exception as e:
            print(f"[turn] stt failed: {type(e).__name__}")  # the error text stays out of the reply and the log
            raise HTTPException(502, "Speech service failed, please type instead.")
    else:
        said, hint = text.strip()[:guard.MAX_TEXT], None
    if not said:
        raise HTTPException(400, "Nothing heard, please try again.")

    if lang:
        case["language"] = lang
    out, speak = flow.advance(case, history, said, lang_hint=hint)
    try:
        out["audio"] = base64.b64encode(gnani.tts(speak, flow.lang(out["case"]))).decode()
    except Exception:
        out["audio"] = None  # text is still on screen; voice is a bonus
    return out
