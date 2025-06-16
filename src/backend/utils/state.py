from typing_extensions import TypedDict
from typing import Dict, Union, List, BinaryIO, Any, Annotated, Optional

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class ExtractorState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    file_input: Union[BinaryIO, bytes, str]
    company_id: str
    company_name:str
    year: str
    esg_report: Dict[str, Any]
    token_usage: Dict[str, int]
    extraction_status: str
    db_status: str
    human_review: bool
    remaining_steps: int
    company_metadata: Dict[str, Any]
    peer_companies: Dict[str, Any]
    esg_report_urls: List[str]

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    remaining_steps: Optional[list]



