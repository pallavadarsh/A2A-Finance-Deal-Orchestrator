from typing import Literal, TypedDict, Optional, Dict, Any
import uuid

MsgType = Literal["PROPOSE","REQUEST","INFORM","ACCEPT","REJECT","ADVISE","ACK","HUMAN_APPROVE","HUMAN_REVISE"]

class A2AMessage(TypedDict, total=False):
    sender: str
    recipient: str
    type: MsgType
    payload: Dict[str, Any]
    corr_id: str
    in_reply_to: Optional[str]

def new_message(sender: str, recipient: str, type: MsgType, payload: Dict[str, Any], in_reply_to: str|None=None) -> A2AMessage:
    return {
        "sender": sender,
        "recipient": recipient,
        "type": type,
        "payload": payload,
        "corr_id": str(uuid.uuid4()),
        "in_reply_to": in_reply_to,
    }
