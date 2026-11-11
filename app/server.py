"""Golden Hour API. Run: python3 -m uvicorn app.server:app --reload  -> http://127.0.0.1:8000

WS /ws/call is the live call (streaming STT/TTS, see app/stream.py).
POST /turn is the fallback: one recorded clip or typed line per request; the browser keeps the case.
"""
import base64
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, WebSocket
from fastapi.responses import FileResponse

from app import flow, gnani, stream

app = FastAPI(title="Golden Hour")
UI = Path(__file__).parent / "static" / "index.html"


@app.get("/")
def index():
    return FileResponse(UI)


@app.websocket("/ws/call")
async def ws_call(ws: WebSocket):
    await stream.run(ws)


@app.post("/turn")
def turn(case: str = Form("{}"), history: str = Form(""), text: str = Form(""),
         audio: Optional[UploadFile] = File(None)):
    if audio is not None:
        try:
            said = gnani.stt(audio.file.read(), audio.filename or "audio.wav", history)["transcript"]
        except Exception as e:
            raise HTTPException(502, f"Speech service failed, please type instead: {e}")
    else:
        said = text.strip()
    if not said:
        raise HTTPException(400, "Nothing heard, please try again.")

    out, speak = flow.advance(json.loads(case or "{}"), history, said)
    try:
        out["audio"] = base64.b64encode(gnani.tts(speak, out["case"].get("language") or "hi")).decode()
    except Exception:
        out["audio"] = None  # text is still on screen; voice is a bonus
    return out
