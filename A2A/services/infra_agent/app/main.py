from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from .protocol import new_message

app=FastAPI(title="InfraAgent")

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
    m=inp.message; fix={"fix":"Shard DB","eta":21}
    return {"outbound":[
        new_message("InfraAgent","RiskAgent","INFORM",fix,in_reply_to=m.get("corr_id")),
        new_message("InfraAgent","RiskAgent","PROPOSE",fix,in_reply_to=m.get("corr_id"))
    ]}
