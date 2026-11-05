"""Golden Hour API. Run: python3 -m uvicorn app.server:app --reload  -> http://127.0.0.1:8000

One endpoint drives the whole conversation; the browser keeps the case and sends it back each turn.
"""
import base64
import json
import re
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app import flow, gnani, rules
from app.extract import extract

app = FastAPI(title="Golden Hour")
UI = Path(__file__).parent / "static" / "index.html"


@app.get("/")
def index():
    return FileResponse(UI)


def _missing(case: dict) -> Optional[str]:
    return next((f for f in flow.ASK_ORDER if case.get(f) is None), None)


@app.post("/turn")
def turn(case: str = Form("{}"), history: str = Form(""), text: str = Form(""),
         audio: Optional[UploadFile] = File(None)):
    case = {**flow.new_case(), **json.loads(case or "{}")}
    if audio is not None:
        try:
            said = gnani.stt(audio.file.read(), audio.filename or "audio.wav", history)["transcript"]
        except Exception as e:
            raise HTTPException(502, f"Speech service failed, please type instead: {e}")
    else:
        said = text.strip()
    if not said:
        raise HTTPException(400, "Nothing heard, please try again.")

    asked = _missing(case) if history.strip() else None  # first turn answers no question
    got = extract(said)
    # A bare "40,000" answering "how much?" has no ₹/rupee word for the rules to anchor on.
    if asked == "amount" and got["amount"] is None:
        nums = [n for n in re.findall(r"\d[\d,]*", rules._join_spaced_digits(said))
                if len(n.replace(",", "")) <= 8]  # skip phone/UTR
        got["amount"] = nums[0] if nums else None
    case = flow.merge(case, got, said)

    question = flow.next_question(case)
    out = {"transcript": said, "case": case, "question": question}
    if question:
        speak = question
    else:
        out["checklist"] = flow.checklist(case)
        out.update(flow.complaint(case))
        speak = " ".join(out["checklist"])
    try:
        out["audio"] = base64.b64encode(gnani.tts(speak, case.get("language") or "hi")).decode()
    except Exception:
        out["audio"] = None  # text is still on screen; voice is a bonus
    return out
