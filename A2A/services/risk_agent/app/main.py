from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from .protocol import new_message

app=FastAPI(title="RiskAgent")

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class In(BaseModel): message: Dict[str, Any]

@app.post("/a2a/message")
def handle(inp: In):
    m = inp.message
    out = []

    if m["type"] == "PROPOSE" and "valuation" in m["payload"]:
        valuation = m["payload"]["valuation"]
        price = valuation.get("price", 0.0)
        ev_ebitda = valuation.get("ev_ebitda", 0.0)

        # --- Risk scoring logic ---
        risk_level = "moderate"
        if price > 300 or ev_ebitda > 12:
            risk_level = "elevated"

        # Kick off tech & security checks
        out.append(new_message("RiskAgent", "DiagnosticsAgent", "REQUEST", {"check": "latency"}))
        out.append(new_message("RiskAgent", "SecurityAgent", "REQUEST", {"scope": "controls"}))

        # Also send preliminary risk assessment to Committee
        out.append(new_message("RiskAgent", "CommitteeAgent", "INFORM", {"risk_level": risk_level}))
        return {"outbound": out}

    if m["type"] in ("INFORM","ADVISE"):
        if m["sender"] == "InfraAgent":
            out.append(new_message("RiskAgent","CommitteeAgent","INFORM",
                                   {"risk_level": "moderate", "note": "Infra remediation proposed"}))
        return {"outbound": out}

    return {"outbound": out}