import os
import json
from typing import List, Dict, Optional

from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from google import genai

from langgraph.prebuilt import create_react_agent

from src.backend.utils.logger import get_logger
from src.backend.utils.common_functions import is_valid_metadata, clean_json_output
from src.backend.utils.system_prompts import build_peer_prompt, build_prompt_for_company, SCRAPER_SYSTEM_PROMPT
from src.backend.services.tavily_service import fetch_info_from_tavily

logger = get_logger()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_MODEL_FOR_PEERS = 'gemini-2.0-flash'

def fetch_company_metadata(company_name: str) -> Optional[Dict[str, str]]:
    """
    Fetches GICS metadata (sector, industry, region, country, etc.) for a given company
    using a combination of web search and LLM interpretation.

    This metadata is essential for downstream tasks like peer comparison.

    Args:
        company_name (str): Name of the target company (e.g., "Tesla", "Nestle").

    Returns:
        Optional[Dict[str, str]]: A dictionary containing metadata such as:
        - "company_name": "Full legal name of the company.",
        - "sector": "GICS sector name (from MSCI definitions).",
        - "industry": "GICS industry name aligned with the core activity.",
        - "headquarters": "City and country of the company`s global headquarters.",
        - "country": "Country of the company`s headquarters.",
        - "region": "Geographic region (e.g., 'North America', 'Europe', 'Asia-Pacific')."

        Returns `None` if metadata cannot be retrieved or fails validation.
    """
    logger.info(f"Fetching GICS metadata for company: {company_name}")

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        search_tool = Tool(google_search=GoogleSearch())

        prompt = build_prompt_for_company(company_name)
        config = GenerateContentConfig(tools=[search_tool], response_modalities=["TEXT"], temperature=0)

        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt, config=config)
        raw_output = ''.join(part.text for part in response.candidates[0].content.parts if hasattr(part, 'text'))
        cleaned_output = clean_json_output(raw_output)

        metadata = json.loads(cleaned_output)

        logger.info(f"Response : {metadata}")
        
        if is_valid_metadata(metadata):
            logger.info(f"Metadata retrieval successful for {company_name}")
            return metadata
        else:
            logger.warning(f"Metadata validation failed for {company_name}")
            return None

    except json.JSONDecodeError as je:
        logger.error(f"[JSONDecodeError] Failed to parse model output: {je}")
    except Exception as e:
        logger.error(f"[Exception] Failed to fetch metadata for {company_name}: {e}")

    return None

def get_peer_companies(metadata: dict, num_country_peers: int = 5, num_region_peers: int = 5) -> Dict[str, List[Dict[str, str]]]:
    """
    Retrieve ESG peer companies for a given company.

    Args:
        metadata (dict): Company metadata including company_name, headquarters, sector, industry, region.
        num_country_peers (int): Number of country-level peers to retrieve.
        num_region_peers (int): Number of regional-level peers to retrieve.

    Returns:
        Dict[str, List[Dict[str, str]]]: Dictionary with peers grouped by geography.
    """
    if not metadata:
        logger.error("Aborting peer analysis due to missing metadata.")
        return {}

    company_name = metadata.get('company_name', 'Unknown Company')
    logger.info(f"Initiating peer analysis for '{company_name}'. "
                f"Country peers: {num_country_peers}, Region peers: {num_region_peers}")

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        search_tool = Tool(google_search=GoogleSearch())

        fetch_country_peers = num_country_peers > 0
        fetch_region_peers = num_region_peers > 0

        if not fetch_country_peers and not fetch_region_peers:
            logger.warning("Both country and region peer counts are 0. Defaulting to 5 for each.")
            num_country_peers = 5
            num_region_peers = 5
            fetch_country_peers = fetch_region_peers = True

        prompt = build_peer_prompt(
            metadata=metadata,
            num_country_peers=num_country_peers if fetch_country_peers else 0,
            num_region_peers=num_region_peers if fetch_region_peers else 0
        )

        config = GenerateContentConfig(
            tools=[search_tool],
            response_modalities=["TEXT"],
            temperature=0
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL_FOR_PEERS,
            contents=prompt,
            config=config
        )

        raw_output = ''.join(
            part.text for part in response.candidates[0].content.parts if hasattr(part, 'text')
        )
        cleaned_output = clean_json_output(raw_output)
        peer_data = json.loads(cleaned_output)

        logger.info(f"Peer companies retrieved successfully: {json.dumps(peer_data, indent=2)}")
        return peer_data

    except json.JSONDecodeError as je:
        logger.error(f"[JSONDecodeError] Failed to parse peer data: {je}")
    except Exception as e:
        logger.error(f"[Exception] Failed to retrieve peer companies: {e}", exc_info=True)

    return {}

def get_company_sustainability_report(company: str, year: Optional[int] = None) -> List[str]:
    """
    Fetches URLs of the company's sustainability report (PDF) for a given year.
    
    Args:
        company (str): Name of the company.
        year (Optional[int]): Year of the sustainability report (optional).
        
    Returns:
        List[str]: List of URLs pointing to PDF files of the sustainability reports.
    """
    logger.info(f"Searching for sustainability report for '{company}'" + (f" in {year}" if year else ""))

    def build_query(company: str, year: Optional[int]) -> str:
        base_query = f"{company} sustainability report"
        if year:
            base_query += f" {year}"
        query = f"{base_query} filetype:pdf"
        logger.info(f"Constructed search query: '{query}'")
        return query

    try:
        query = build_query(company, year)
        response = fetch_info_from_tavily(query)
        logger.info(f"Response : {response}")
        
        if not response or 'results' not in response:
            logger.warning("No results found or invalid response structure.")
            return []

        urls = [res.get("url") for res in response['results'] if res.get("url")]
        logger.info(f"Found {len(urls)} report(s) for '{company}'")
        return urls

    except Exception as e:
        logger.error(f"Error while fetching report for '{company}': {e}", exc_info=True)
        return []


def initialize_scraper():
    scraper_assistant = create_react_agent(
        model="openai:gpt-4o-mini",
        tools=[fetch_company_metadata, get_peer_companies, get_company_sustainability_report],
        prompt=SCRAPER_SYSTEM_PROMPT,
        name="scraper_assistant"
    )
    return scraper_assistant

# metadata = fetch_company_metadata("Yuvabe")
# result = get_peer_companies(metadata)
# print(result)

# report = get_company_sustainability_report(company="Infosys")
# print(report)

# metadata =  {
# 'company_name': 'Yuvabe', 
# 'core': 'Empowering youth through education, STEAM programs, and digital transformation services with a Work. Serve. Evolve. model.', 
# 'sector': 'Consumer Discretionary', 
# 'industry': 'Education Services',
# 'headquarters': 'Auroville, India',
# 'country': 'India', 
# 'region': 'Asia-Pacific'
# }

# metadata =  {
#     "company_name": "Zalando SE",
#     "sector": "Consumer Discretionary",
#     "industry": "Internet & Direct Marketing Retail",
#     "headquarters": "Berlin, Germany",
#     "country": "Germany",
#     "region": "Europe"
#   }
# result = get_peer_companies(metadata,num_country_peers=1, num_region_peers=2)
# print(result)

# result = get_company_sustainability_report("Yuvabe")
# print(result)