from typing import List, Dict, Optional


from langgraph.prebuilt import create_react_agent

from src.backend.utils.logger import get_logger
from src.backend.utils.system_prompts import build_peer_prompt, build_company_classification_prompt, SCRAPER_SYSTEM_PROMPT
from src.backend.services.tavily_service import fetch_info_from_tavily
from src.backend.models.schemas import CompanyMetadata
from src.backend.models.gics_schema import GICS_CLASSIFICATION_SCHEMA
from src.backend.services.openai_service import get_openai_client
from src.backend.services.gemini_service import get_gemini_client
from src.backend.config.constants import OPENAI_MODEL

logger = get_logger()

openai_client =  get_openai_client()
gemini_client = get_gemini_client()

def fetch_company_metadata(company_name: str, content: Optional[List[str]] = None) -> Optional[CompanyMetadata]:
    """
        Classifies a company using the GICS schema based on unstructured web data.

        Args:
            company_name (str): Name of the company to classify.
            content (List[str], optional): Pre-fetched content. If not provided, it fetches using Tavily.

        Returns:
            Optional[CompanyMetadata]: Parsed company metadata if successful, else None.
    """
    try:
        if not content:
            query = f"What does {company_name} do and where is it located?"
            response = fetch_info_from_tavily(query=query)
            if not response or 'results' not in response:
                logger.error(f"No results found for company: '{company_name}'")
                return None

            content = [
                res.get("content")
                for res in response['results']
                if res.get("content")
            ]

        if not content:
            logger.error(f"No usable content found to classify company: '{company_name}'")
            return None

        logger.info(f"Building classification prompt for company: '{company_name}'")
        messages = build_company_classification_prompt(content, GICS_CLASSIFICATION_SCHEMA)

        completion = openai_client.responses.parse(
            model=OPENAI_MODEL,
            input=messages,
            text_format=CompanyMetadata,
            temperature=0,
        )
        return completion.output_parsed

    except Exception as e:
        logger.error(f"Error classifying company '{company_name}': {e}", exc_info=True)
        return None

def get_peer_companies(
    metadata: CompanyMetadata,
    num_country_peers: Optional[int] = None,
    num_region_peers: Optional[int] = None
) -> Dict[str, List[Dict[str, str]]]:
    """
    Retrieve ESG peer companies for a given company using GICS metadata.

    Args:
        metadata (CompanyMetadata): Includes company_name, sector, industry_group,
                                    industry, sub_industries, headquarters, country, region.
        num_country_peers (Optional[int]): Number of country-level peers to retrieve.
        num_region_peers (Optional[int]): Number of regional-level peers to retrieve.

    Returns:
        Dict[str, List[Dict[str, str]]]: Dictionary with keys "country_peers" and/or "region_peers".
    """
    if not metadata:
        logger.error("Aborting peer analysis: metadata is None.")
        return {}
    
    if num_country_peers is None and num_region_peers is None:
        num_country_peers = 5
        num_region_peers = 5
    elif num_country_peers and not num_region_peers:
        num_region_peers = 0
    elif num_region_peers and not num_country_peers:
        num_country_peers = 0
    elif num_country_peers <= 0 and num_region_peers <= 0:
        logger.warning("Both peer counts are 0. Defaulting to 5 each.")
        num_country_peers = num_region_peers = 5

    logger.info(f"Initiating peer analysis for '{metadata.company_name}'. "
                f"Country peers: {num_country_peers}, Region peers: {num_region_peers}")
    
    try:

        prompt = build_peer_prompt(
            company_name=metadata.company_name,
            sector=metadata.sector,
            industry_group=metadata.industry_group,
            industry=metadata.industry,
            sub_industries=metadata.sub_industries,
            headquarters=metadata.headquarters,
            country=metadata.country,
            region=metadata.region,
            num_country_peers=num_country_peers,
            num_region_peers=num_region_peers
        )


        response = openai_client.responses.create(
            model="gpt-4.1",
            tools=[{
                "type": "web_search_preview",
                "search_context_size": "low",
            }],
            input=prompt,
            temperature=0
        )
        result = response.output_text
        logger.info(f"Result : {result}")
        return result

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

    try:
        base_query = f"{company} sustainability report"
        query = f"{base_query} {year} filetype:pdf" if year else f"{base_query} filetype:pdf"
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
    """
    Initializes a React-style scraper agent that utilizes the fetch_company_metadata, get_peer_companies,
    and get_company_sustainability_report tools.
    """
    return create_react_agent(
        model="openai:gpt-4o-mini",
        tools=[fetch_company_metadata, get_peer_companies, get_company_sustainability_report],
        prompt=SCRAPER_SYSTEM_PROMPT,
        name="scraper_assistant"
    )