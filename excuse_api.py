# excuse_api.py
import os, json, time, hashlib
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)



from fastapi import FastAPI
from pydantic import BaseModel

# --- Gemini via LangChain (REST v1) ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

# expose key for LangChain wrapper
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")  # must be in .env

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",          # free‑tier model
    temperature=0.8,
    convert_system_message_to_human=True
)
#print(">>> model being used:", model._name) 
# ---------- simple “DB” ----------
DATA = Path("history.json")
if not DATA.exists():
    DATA.write_text("[]")          # seed empty list



# ---------- FastAPI app ----------
app = FastAPI()

class Req(BaseModel):
    scenario: str  # e.g. "missed class"
    urgency: str   # "low" | "medium" | "panic"
    mode: str = "normal"   # "normal" | "apology"
    language: str = "en"   # ISO code, e.g. "en", "es", "fr"

class EmergencyRequest(BaseModel):
    number: str
    message: str

SYSTEM_PROMPT = """
You are an elite alibi-creator.
Return a JSON with:
  excuse               (≤ 50 words),
  believability_score  (0-1),
  chat_log             (short WhatsApp-style proof)
"""

# ---------- /generate ----------
@app.post("/generate")
def generate(r: Req):
    style_clause = (
        "Respond in a guilt‑tripping, heartfelt apology tone."
        if r.mode.lower() == "apology"
        else "Respond in a neutral, believable tone."
    )
    # language directive
    lang_clause = (
        "" if r.language.lower() in ["en", "english"] else
        f"Respond in {r.language} language."
    )
    full_prompt = (
        f"{SYSTEM_PROMPT}\n"
        f"Tone: {style_clause}\n"
        f"{lang_clause}\n"
        f"Scenario: {r.scenario}\nUrgency: {r.urgency}"
    )
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=full_prompt)
    ]
    response_text = llm(messages).content.strip()
    # LangChain may wrap JSON in ``` blocks – strip them
    if response_text.startswith("```"):
        response_text = response_text.strip("`").lstrip("json").strip()
    out = json.loads(response_text)
    entry = {
        "id": hashlib.md5(out["excuse"].encode()).hexdigest(),
        "ts": time.time(),
        **out,
    }

    history = json.loads(DATA.read_text())
    if entry["id"] not in {h["id"] for h in history}:   # de-dupe
        history.append(entry)
        DATA.write_text(json.dumps(history, indent=2))

    return entry

# ---------- /top?n=5 ----------
@app.get("/top")
def top(n: int = 5):
    history = json.loads(DATA.read_text())
    history.sort(key=lambda x: x["believability_score"], reverse=True)
    return history[:n]

# ---------- /emergency ----------
@app.post("/emergency")
def emergency(req: EmergencyRequest):
    """
    Simulate sending an emergency SMS/call.
    For the demo we just log the request and append an entry to history.json.
    """
    entry = {
        "id": f"emergency-{int(time.time())}",
        "ts": time.time(),
        "excuse": "EMERGENCY TRIGGER",
        "believability_score": 1.0,
        "chat_log": f"Sent '{req.message}' to {req.number}"
    }
    history = json.loads(DATA.read_text())
    history.append(entry)
    DATA.write_text(json.dumps(history, indent=2))
    return {"status": "sent", "to": req.number, "msg": req.message}