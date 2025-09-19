
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import os, requests

from .protocol import new_message

app = FastAPI(title="CommitteeAgent")
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Call Groq LLM (if API key is set) ---
def llm_call(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return f"[MOCK MEMO] {prompt[:200]}"

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
                "messages": [
                    {"role": "system", "content": "You are an Investment Committee assistant. Summarize risk and legal findings into a crisp memo."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 300,
            },
            timeout=30,
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[LLM ERROR: {e}] {prompt[:200]}"

class InMsg(BaseModel):
    message: Dict[str, Any]

@app.post("/a2a/message")
def handle(inp: InMsg):
    m = inp.message
    out = []

    # --- When Risk + Legal INFORM arrives ---
    if m["type"] == "INFORM" and "risk" in m["payload"] and "legal" in m["payload"]:
        prompt = f"Draft Investment Memo. Risk findings: {m['payload']['risk']}. Legal findings: {m['payload']['legal']}."
        draft = llm_call(prompt)
        out.append(new_message("CommitteeAgent", "Orchestrator", "INFORM",
                               {"draft_memo": draft}, in_reply_to=m.get("corr_id")))
        return {"outbound": out}

    # --- When Human-in-the-Loop decision arrives ---
    msg_type = m["type"].upper()
    if msg_type in ("HUMAN_APPROVE", "HUMAN_REVISE"):
        notes = m.get("payload", {}).get("notes", "")
        prompt = f"Finalize Investment Memo. Human feedback: {notes}."
        final = llm_call(prompt)
        out.append(new_message(
            "CommitteeAgent", "Orchestrator", "INFORM",
            {"final_memo": final},
            in_reply_to=m.get("corr_id")
        ))
        return {"outbound": out}
    

    return {"outbound": []}
