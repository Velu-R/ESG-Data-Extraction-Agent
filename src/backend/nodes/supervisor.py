from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage


from src.backend.nodes.scraper import initialize_scraper
from src.backend.nodes.extractor import initialize_extractor_agent
from src.backend.utils.system_prompts import SUPERVISOR_SYSTEM_PROMPT

scraper_agent= initialize_scraper()
extractor_agent = initialize_extractor_agent()

supervisor = create_supervisor(
    agents=[scraper_agent, extractor_agent],
    model=ChatOpenAI(model="gpt-4o-mini"),
    prompt=SUPERVISOR_SYSTEM_PROMPT,
).compile()

# input_message = {
#     "messages": [
#         {"role": "user", "content": "Can you get Zalando and it's peers metadata"}
#     ]
# }

# result = supervisor.invoke(input_message)

# messages = result['messages']

# ai_messages = []
# tool_messages = []

# for msg in messages:
#     if isinstance(msg, AIMessage):
#         ai_messages.append(msg)
#     elif isinstance(msg, ToolMessage):
#         tool_messages.append(msg)

# # Log AI messages
# print("=== AI MESSAGES ===")
# for ai in ai_messages:
#     print(f"\nFrom: {ai.name}")
#     print(f"Content: {ai.content}")
#     print(f"Tool Calls: {getattr(ai, 'tool_calls', 'None')}")
#     print("-----")

# # Log Tool messages
# print("=== TOOL MESSAGES ===")
# for tool in tool_messages:
#     print(f"\nFrom Tool: {tool.name}")
#     print(f"Content: {tool.content}")
#     print("-----")