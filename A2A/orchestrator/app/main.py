
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import requests, time, uuid

from .core.protocol import A2AMessage, new_message

app = FastAPI(title="A2A Orchestrator")


from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Service registry (Docker Compose service names + ports) ---
REGISTRY = {
    "FinanceAgent": "http://finance_agent:8101/a2a/message",
    "RiskAgent": "http://risk_agent:8102/a2a/message",
    "LegalAgent": "http://legal_agent:8103/a2a/message",
    "DiagnosticsAgent": "http://diagnostics_agent:8104/a2a/message",
    "InfraAgent": "http://infra_agent:8105/a2a/message",
    "SecurityAgent": "http://security_agent:8106/a2a/message",
    "CommitteeAgent": "http://committee_agent:8107/a2a/message",
}

# --- State ---
RUNS: Dict[str, Dict[str, Any]] = {}

class DealBrief(BaseModel):
    deal_name: str
    target: Dict[str, Any]
    financials: Dict[str, float]
    purchase_price: float
    currency: str = "USD"
    notes: Optional[str] = None

class StartOut(BaseModel):
    run_id: str
    draft: str

class FinalOut(BaseModel):
    run_id: str
    final: str

def log_event(run_id: str, event: Dict[str, Any]):
    event.setdefault("ts", time.time())
    RUNS.setdefault(run_id, {"events": [], "context": {}, "queue": []})["events"].append(event)

def dispatch(run_id: str, msg: A2AMessage):
    """Send one message to its recipient service."""
    url = REGISTRY[msg["recipient"]]
    log_event(run_id, {"kind": "protocol", **msg})
    r = requests.post(url, json={"message": msg}, timeout=30)
    r.raise_for_status()
    return r.json().get("outbound", [])

def route_loop(run_id: str):
    """Route messages until we reach Draft or Final stage."""
    ctx = RUNS[run_id]["context"]
    q: List[A2AMessage] = RUNS[run_id]["queue"]

    while q:
        msg = q.pop(0)
        outbound = dispatch(run_id, msg)
        q.extend(outbound)

        # Collect risk/legal separately
        if msg["sender"] == "RiskAgent" and msg["recipient"] == "CommitteeAgent":
            ctx["risk"] = msg["payload"]
        if msg["sender"] == "LegalAgent" and msg["recipient"] == "CommitteeAgent":
            ctx["legal"] = msg["payload"]

        # If we have both risk + legal, send a combined INFORM to Committee
        if ctx.get("risk") and ctx.get("legal") and not ctx.get("draft_sent"):
            combined = new_message(
                "Orchestrator",
                "CommitteeAgent",
                "INFORM",
                {"risk": ctx["risk"], "legal": ctx["legal"]},
            )
            q.append(combined)
            ctx["draft_sent"] = True

        # Draft memo arrives
        if msg["sender"] == "CommitteeAgent" and "draft_memo" in msg["payload"]:
            ctx["draft"] = msg["payload"]["draft_memo"]
            return {"stage": "DRAFT", "draft": ctx["draft"]}

        # Final memo arrives
        if msg["sender"] == "CommitteeAgent" and "final_memo" in msg["payload"]:
            ctx["final"] = msg["payload"]["final_memo"]
            log_event(run_id, {"kind": "protocol", **msg})  # ensure it shows up in /trace
            return {"stage": "FINAL", "final": ctx["final"]}


    return {"stage": "IDLE"}

@app.post("/deal/start", response_model=StartOut)
def start(deal: DealBrief):
    run_id = str(uuid.uuid4())
    RUNS[run_id] = {"events": [], "context": {}, "queue": []}

    # Kickoff → IntakeAgent REQUEST to FinanceAgent
    first = new_message("IntakeAgent", "FinanceAgent", "REQUEST",
                        {"goal": "Evaluate", "deal": deal.model_dump()})
    RUNS[run_id]["queue"].append(first)

    res = route_loop(run_id)
    if res.get("stage") != "DRAFT":
        raise HTTPException(500, f"Did not reach draft stage. Got: {res}")
    return {"run_id": run_id, "draft": res["draft"]}

class HumanReview(BaseModel):
    run_id: str
    decision: str  # "approve" | "revise"
    feedback: Optional[str] = None

@app.post("/deal/review", response_model=FinalOut)
def review(hr: HumanReview):
    st = RUNS.get(hr.run_id)
    if not st:
        raise HTTPException(404, "Unknown run_id")

    # Send human decision to Committee
    if hr.decision.lower() == "approve":
        msg = new_message("HumanReviewer", "CommitteeAgent",
                          "HUMAN_APPROVE", {"notes": hr.feedback or ""})
    else:
        msg = new_message("HumanReviewer", "CommitteeAgent",
                          "HUMAN_REVISE", {"notes": hr.feedback or ""})
    st["queue"] = [msg]

    res = route_loop(hr.run_id)
    if res.get("stage") != "FINAL":
        raise HTTPException(500, f"Did not reach final stage. Got: {res}")
    return {"run_id": hr.run_id, "final": res["final"]}

@app.get("/trace/{run_id}/timeline")
def timeline(run_id: str):
    ev = RUNS.get(run_id, {}).get("events", [])
    return {
        "timeline": [
            f"{e['sender']} —{e['type']}→ {e['recipient']} | {str(e['payload'])[:200]}"
            for e in ev if e.get("kind") == "protocol"
        ]
    }
