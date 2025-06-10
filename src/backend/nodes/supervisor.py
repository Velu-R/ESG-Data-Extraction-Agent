from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI

from src.backend.nodes.scraper import initialize_scraper
from src.backend.nodes.extractor import initialize_extractor_agent
from src.backend.utils.system_prompts import SUPERVISOR_SYSTEM_PROMPT
from src.backend.agent.graph import generate_query


scraper_agent= initialize_scraper()
extractor_agent = initialize_extractor_agent()

supervisor = create_supervisor(
    agents=[scraper_agent, extractor_agent],
    model=ChatOpenAI(model="gpt-4o-mini"),
    prompt=SUPERVISOR_SYSTEM_PROMPT,
).compile()