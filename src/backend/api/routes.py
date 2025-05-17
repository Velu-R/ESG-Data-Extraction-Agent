from fastapi import APIRouter, HTTPException
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage, BaseMessage
from typing import Dict
import os

from src.backend.models.schemas import Message, InputPayload, MessageResponse
from src.backend.nodes.supervisor import supervisor

from src.backend.utils.logger import get_logger

logger = get_logger()
router = APIRouter()

def to_langchain_message(msg: Message) -> BaseMessage:
    match msg.role:
        case "user":
            return HumanMessage(content=msg.content)
        case "assistant":
            return AIMessage(content=msg.content)
        case "system":
            return SystemMessage(content=msg.content)
        case _:
            raise ValueError(f"Unsupported message role: {msg.role}")

def serialize_message(msg: BaseMessage) -> Dict:
    return {
        "type": msg.__class__.__name__,
        "content": msg.content
    }

@router.post("/invoke-supervisor", response_model=MessageResponse, summary="Invoke Supervisor Agent", tags=["Supervisor"])
async def invoke_supervisor(input_payload: InputPayload):
    try:
        # LANGSMITH_API_KEY=os.getenv('LANGSMITH_API_KEY')
        # os.environ['LANGSMITH_API_KEY'] = LANGSMITH_API_KEY
        # os.environ['LANGCHAIN_TRACING_V2'] = 'true'
        # os.environ["LANGCHAIN_PROJECT"] = "Sustainability_AI"
        logger.info("Received request for supervisor.")
        langchain_messages = [to_langchain_message(msg) for msg in input_payload.messages]
        result = supervisor.invoke({"messages": langchain_messages})

        messages = result.get("messages", [])

        ai_messages = [serialize_message(m) for m in messages if isinstance(m, AIMessage)]
        tool_messages = [serialize_message(m) for m in messages if isinstance(m, ToolMessage)]
        human_messages = [serialize_message(m) for m in messages if isinstance(m, HumanMessage)]

        return MessageResponse(
            ai_messages=ai_messages,
            tool_messages=tool_messages,
            human_messages=human_messages
        )

    except Exception as e:
        logger.exception("Supervisor invocation failed")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("/", summary="Health check", tags=["Health"])
async def health_check():
    return {"message": "Service is running"}
