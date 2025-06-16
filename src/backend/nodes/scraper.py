from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

from src.backend.utils.logger import get_logger
from src.backend.utils.system_prompts import build_peer_prompt, build_company_classification_prompt, SCRAPER_SYSTEM_PROMPT
from src.backend.services.tavily_service import fetch_info_from_tavily
from src.backend.models.schemas import CompanyMetadata
from src.backend.models.gics_schema import GICS_CLASSIFICATION_SCHEMA
from src.backend.services.openai_service import get_openai_client
from src.backend.services.gemini_service import get_gemini_client
from src.backend.config.config import config
from src.backend.utils.state import ExtractorState, AgentState

from src.backend.tools.tool import fetch_company_metadata, get_peer_companies, get_company_sustainability_report


logger = get_logger()

openai_client =  get_openai_client()
gemini_client = get_gemini_client()

# @tool
# def fetch_company_metadata(state: ExtractorState) -> ExtractorState:
#     """
#     Fetches and classifies company metadata using unstructured data and the GICS schema.
#     Updates the state with 'company_metadata' if classification is successful.

#     Args:
#         state (ExtractorState): The agent's current state containing 'company_name'.

#     Returns:
#         ExtractorState: Updated state with 'company_metadata' and messages.
#     """
#     state = dict(state or {})
#     company_name = state.get("company_name")
#     messages = state.get("messages", [])

#     if not company_name:
#         logger.info("Missing 'company_name' in state.")
#         return None
    
#     try:
#         query = f"What does {company_name} do and where is it located?"
#         response = fetch_info_from_tavily(query=query)

#         if not response or 'results' not in response:
#             logger.error(f"No results found for company: '{company_name}'")
#             return None

#         content = [res.get("content") for res in response['results'] if res.get("content")]     

#         if not content:
#             logger.error(f"No usable content found to classify company: '{company_name}'")
#             return None

#         logger.info(f"Building classification prompt for company: '{company_name}'")
#         messages_for_llm  = build_company_classification_prompt(content, GICS_CLASSIFICATION_SCHEMA)

#         completion = openai_client.responses.parse(
#             model=config.OPENAI_MODEL,
#             input=messages_for_llm ,
#             text_format=CompanyMetadata,
#             temperature=0,
#         )

#         parsed_metadata = completion.output_parsed
#         logger.info(f"Successfully parsed metadata for '{company_name}': {parsed_metadata}")
#         state["company_metadata"] = parsed_metadata.model_dump()
#         state["messages"] = messages + [{"role": "system", "content": "Company metadata classification succeeded."}]
#         return state

#     except Exception as e:
#         logger.error(f"Error classifying company '{company_name}': {e}", exc_info=True)
#         return None

# @tool
# def get_peer_companies(state: ExtractorState) -> ExtractorState:
#     """
#     Retrieves peer companies using GICS classification from the state metadata.
#     Updates state with 'peer_companies'.

#     Args:
#         state (ExtractorState): The agent's shared state.
#             Required keys in `state`:
#             - company_metadata (dict): Must include:
#                 - company_name (str)
#                 - sector (str)
#                 - industry_group (str)
#                 - industry (str)
#                 - sub_industries (Union[str, List[str]])
#                 - headquarters (str)
#                 - country (str)
#                 - region (str)

#             Optional keys:
#             - messages (List[dict]): Message history.

#     Returns:
#         ExtractorState: Updated state with 'peer_companies' and updated messages.
#     """
#     try:
#         state = dict(state or {})
#         messages = state.get("messages", [])

#         metadata_dict = state.get("company_metadata")
#         if not metadata_dict:
#             logger.info("Missing 'company_metadata' in state.")
#             return state

#         # --- Normalize metadata fields ---
#         if isinstance(metadata_dict.get("sub_industries"), list):
#             metadata_dict["sub_industries"] = ", ".join(metadata_dict["sub_industries"])

#         # Provide default or fallback for missing optional fields if needed
#         metadata_dict.setdefault("core", "N/A")  # fallback if your model expects it

#         # --- Validate and parse ---
#         metadata = CompanyMetadata(**metadata_dict)
#         logger.info(f"Initiating peer analysis for '{metadata.company_name}'")

#         # --- Construct prompt ---
#         prompt = build_peer_prompt(
#             company_name=metadata.company_name,
#             sector=metadata.sector,
#             industry_group=metadata.industry_group,
#             industry=metadata.industry,
#             sub_industries=metadata.sub_industries,
#             headquarters=metadata.headquarters,
#             country=metadata.country,
#             region=metadata.region,
#             num_country_peers=5,
#             num_region_peers=5
#         )

#         # --- OpenAI call ---
#         response = openai_client.responses.create(
#             model="gpt-4.1",
#             tools=[{
#                 "type": "web_search_preview",
#                 "search_context_size": "low",
#             }],
#             input=prompt,
#             temperature=0
#         )
#         result = response.output_text

#         logger.info(f"Peer analysis result for '{metadata.company_name}': {result}")

#         # --- Update state ---
#         state["peer_companies"] = {"raw_output": result}
#         state["messages"] = messages + [{
#             "role": "system",
#             "content": f"Peer companies retrieved successfully for '{metadata.company_name}'."
#         }]

#     except Exception as e:
#         logger.error(f"[Exception] Failed to retrieve peer companies: {e}", exc_info=True)

#     return state

# @tool
# def get_company_sustainability_report(state: ExtractorState) -> ExtractorState:
#     """
#     Fetches URLs of the company's sustainability (ESG) reports (PDFs) based on the company name and optional year.
#     Updates the state with found ESG report URLs and logs progress/errors via messages.

#     Args:
#         state (ExtractorState): The agent's state including company name and optional year.

#     Returns:
#         ExtractorState: Updated state with ESG report URLs and system messages.
#     """
#     try:
#         company_name = state.company_name
#         year = state.year
#         messages = state.messages

#         base_query = f"{company_name} sustainability report"
#         query = f"{base_query} {year} filetype:pdf" if year else f"{base_query} filetype:pdf"

#         logger.info(f"Querying for: {query}")
#         response = fetch_info_from_tavily(query)
#         logger.debug(f"Tavily response: {response}")

#         urls = [res.get("url") for res in response.get("results", []) if res.get("url")]

#         if urls:
#             messages.append({
#                 "role": "system",
#                 "content": f"Found {len(urls)} ESG report(s) for '{company_name}'."
#             })
#             logger.info(f"Found {len(urls)} ESG report(s) for '{company_name}'.")
#         else:
#             messages.append({
#                 "role": "system",
#                 "content": f"No ESG reports found for '{company_name}'."
#             })
#             logger.warning(f"No ESG reports found for '{company_name}'.")

#         return ExtractorState(
#             company_name=company_name,
#             year=year,
#             messages=messages,
#             esg_report_urls=urls
#         )

#     except Exception as e:
#         logger.error(f"Exception during ESG report fetch for '{state.company_name}': {e}", exc_info=True)
#         state.messages.append({
#             "role": "system",
#             "content": f"Error occurred while searching for ESG reports: {str(e)}"
#         })
#         return ExtractorState(
#             company_name=state.company_name,
#             year=state.year,
#             messages=state.messages,
#             esg_report_urls=[]
#         )

def initialize_scraper():
    """
    Initializes a React-style scraper agent that utilizes the fetch_company_metadata, get_peer_companies,
    and get_company_sustainability_report tools.
    """
    return create_react_agent(
        model="openai:gpt-4o-mini",
        tools=[fetch_company_metadata, get_peer_companies, get_company_sustainability_report],
        prompt=SCRAPER_SYSTEM_PROMPT,
        name="scraper_assistant",
        state_schema=AgentState
    )