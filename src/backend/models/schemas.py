from pydantic import BaseModel, Field
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

class CompanyMetadata(BaseModel):
    company_name: str = Field(..., description="Full legal name of the company.")
    core: str = Field(..., description="Primary product, service, or business focus.")
    sector: str = Field(..., description="GICS sector name (from MSCI definitions).")
    industry_group: str = Field(..., description="GICS industry group aligned with the core activity.")
    industry: str = Field(..., description="GICS industry name aligned with the core activity.")
    sub_industries: str = Field(..., description="GICS sub-industry categories relevant to the business.")
    headquarters: str = Field(..., description="City and country of the company`s global headquarters.")
    country: str = Field(..., description="Country of the company`s headquarters.")
    region: str = Field(..., description="Geographic region (e.g., 'North America', 'Europe', 'Asia-Pacific').")

class PeersMetadata(BaseModel):
    peers_metadata: List[CompanyMetadata] = Field(
        ..., description="List of peer companies metadata"
    )
