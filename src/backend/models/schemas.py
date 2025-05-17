from pydantic import BaseModel
from typing import List, Literal, Dict

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class InputPayload(BaseModel):
    messages: List[Message]

class MessageResponse(BaseModel):
    ai_messages: List[Dict]
    tool_messages: List[Dict]
    human_messages: List[Dict]