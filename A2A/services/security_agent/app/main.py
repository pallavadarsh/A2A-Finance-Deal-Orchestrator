from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from .protocol import new_message

app=FastAPI(title="SecurityAgent")
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
    m=inp.message; advice={"controls":["SOC2","Encryption"]}
    return {"outbound":[new_message("SecurityAgent","RiskAgent","ADVISE",advice,in_reply_to=m.get("corr_id"))]}
