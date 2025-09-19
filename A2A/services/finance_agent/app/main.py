from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from .protocol import new_message

app=FastAPI(title="FinanceAgent")

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
    m=inp.message; deal=m["payload"]["deal"]
    e=float(deal["financials"]["ebitda"]); p=float(deal["purchase_price"])
    mult=round(p/e,2)
    return {"outbound":[
        new_message("FinanceAgent","RiskAgent","PROPOSE",{"valuation":{"ev_ebitda":mult,"price":p}},in_reply_to=m.get("corr_id")),
        new_message("FinanceAgent","LegalAgent","INFORM",{"valuation_hint":{"ev_ebitda":mult}},in_reply_to=m.get("corr_id"))
    ]}
