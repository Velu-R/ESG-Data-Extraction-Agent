from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import Runnable

from src.backend.config.llm_factory import LLMFactory
from src.backend.schemas.state import AgentState
from src.backend.utils.system_prompts import (
    EXTRACTOR_AGENT_PROMPT,
    SCRAPER_SYSTEM_PROMPT,
    SUPERVISOR_SYSTEM_PROMPT
)
from src.backend.utils.logger import get_logger
from src.backend.tools.tool import (
    extract_emission_data_as_json,
    upsert_esg_report,
    fetch_company_metadata,
    get_peer_companies,
    get_company_sustainability_report
)
from langgraph_supervisor import create_supervisor

logger = get_logger()

openai_llm = LLMFactory("openai").llm

# ---------- Agent Initialization ----------

def initialize_extractor_agent() -> Runnable:
    """
    Initializes the Extractor Agent.
    This agent uses emission extraction tools to parse ESG reports and persist structured data.
    """
    logger.info("Initializing Extractor Agent...")
    return create_react_agent(
        model=openai_llm,
        tools=[extract_emission_data_as_json, upsert_esg_report],
        prompt=EXTRACTOR_AGENT_PROMPT,
        name="extractor_agent",
        state_schema=AgentState
    )

def initialize_scraper_agent() -> Runnable:
    """
    Initializes the Scraper Agent.
    This agent scrapes company metadata, peers, and ESG report links.
    """
    logger.info("Initializing Scraper Agent...")
    return create_react_agent(
        model=openai_llm,
        tools=[fetch_company_metadata, get_peer_companies, get_company_sustainability_report],
        prompt=SCRAPER_SYSTEM_PROMPT,
        name="scraper_agent",
        state_schema=AgentState
    )

def initialize_supervisor_agent(scraper_agent: Runnable, extractor_agent: Runnable) -> Runnable:
    """
    Initializes the Supervisor Agent to orchestrate between scraper and extractor agents.
    """
    logger.info("Initializing Supervisor Agent...")
    return create_supervisor(
        agents=[scraper_agent, extractor_agent],
        model=openai_llm,
        prompt=SUPERVISOR_SYSTEM_PROMPT,
        state_schema=AgentState,
        output_mode="full_history",
    ).compile()

scraper_agent = initialize_scraper_agent()
extractor_agent = initialize_extractor_agent()
supervisor_graph = initialize_supervisor_agent(scraper_agent, extractor_agent)

