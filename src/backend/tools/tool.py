import json
from typing import Optional, Dict, Union, BinaryIO, Any
import threading
import time

from typing import List, Dict, Optional

from dotenv import load_dotenv

from langchain_core.tools import tool

from src.backend.utils.logger import get_logger
from src.backend.services.gemini_service import upload_file
from src.backend.schemas.esg_schema import (
    ReportMetadata, EnvironmentalEmissionsEnergy, EnvironmentalWaterWaste, SocialTrainingAndCSR, 
    SocialWorkforceAndWellBeing, GovernanceEthicsAndComplaints, GovernanceStructureAndOpenness,
    MaterialityAssessment
)
from src.backend.utils.system_prompts import EXTRACTOR_TOOL_PROMPT
from src.backend.utils.system_prompts import build_peer_prompt, build_company_classification_prompt
from src.backend.services.tavily_service import fetch_info_from_tavily
from src.backend.schemas.scraper_schema import CompanyMetadata
from src.backend.schemas.gics_schema import GICS_CLASSIFICATION_SCHEMA
from src.backend.config.config import config
from src.backend.services.openai_service import get_openai_client
from src.backend.services.gemini_service import get_gemini_client


gemini_client = get_gemini_client()
openai_client=get_openai_client()

RESPONSE_SCHEMA = [
    ReportMetadata,
    EnvironmentalEmissionsEnergy,
    EnvironmentalWaterWaste,
    SocialTrainingAndCSR,
    SocialWorkforceAndWellBeing,
    GovernanceEthicsAndComplaints,
    GovernanceStructureAndOpenness,
    MaterialityAssessment
]

load_dotenv()
logger = get_logger()

thread_local = threading.local()

@tool
def extract_emission_data_as_json(file_input: Union[BinaryIO, bytes, str]) -> Optional[Dict[str, Any]]:
    """
    Tool: ESG Report Extractor

    Uploads and processes a sustainability report (PDF) using the Gemini model to extract structured ESG data.

    This tool:
    - Uploads a report to Gemini.
    - Iteratively extracts predefined ESG schemas.
    - Merges results into a unified JSON object.
    - Tracks Gemini token usage.

    Input:
        file_input (str | bytes | BinaryIO): ESG PDF report.
            - Accepts: local file path, remote URL (ending in .pdf), byte stream.

    Output:
        dict | None:
            {
                "_id": <company_legal_name>,
                "year": <reporting_year>,
                "esg_report": {merged ESG data},
                "token_usage": {
                    "total_prompt_tokens": int,
                    "total_output_tokens": int,
                    "total_tokens": int
                }
            }

    Returns None on failure or if required metadata is missing.
    """
    if not file_input:
        logger.error("No file input provided for ESG extraction.")
        return None

    try:
        uploaded_file = upload_file(file=file_input)
        if not uploaded_file:
            logger.error("File upload to Gemini failed.")
            return None
    except Exception as upload_err:
        logger.error(f"Exception during file upload: {upload_err}")
        return None
    
    if not hasattr(thread_local, "gemini_client"):
        thread_local.gemini_client = gemini_client
    
    client = thread_local.gemini_client

    merged_result: Dict[str, Any] = {}
    token_usage = {
        "total_prompt_tokens": 0,
        "total_output_tokens": 0,
        "total_tokens": 0
    }
    MAX_RETRIES = config.MAX_RETRIES
    RETRY_DELAY_SECONDS = config.RETRY_DELAY_SECONDS

    for schema in RESPONSE_SCHEMA:
        schema_name = getattr(schema, "__name__", str(schema))
        attempt = 0

        while attempt < MAX_RETRIES:
            try:
                response = client.models.generate_content(
                    model=config.GEMINI_EXTRACTION_MODEL,
                    contents=[uploaded_file, EXTRACTOR_TOOL_PROMPT],
                    config={
                        'response_mime_type': 'application/json',
                        'response_schema': schema,
                        'temperature': 0.0,
                    },
                )

                usage = getattr(response, "usage_metadata", None)
                if usage:
                    token_usage["total_prompt_tokens"] += usage.prompt_token_count or 0
                    token_usage["total_output_tokens"] += usage.candidates_token_count or 0
                    token_usage["total_tokens"] += usage.total_token_count or 0

                raw_text = getattr(response, "text", "")
                if not raw_text and getattr(response, "candidates", []):
                    raw_text = response.candidates[0].content.parts[0].text

                if not raw_text:
                    logger.error(f"Empty response for schema '{schema_name}'.")
                    logger.info(f"Raw response (if any): {response}")
                    raise ValueError("Empty Gemini response")

                result_json = json.loads(raw_text)
                if not isinstance(result_json, dict):
                    logger.error(f"Schema '{schema_name}' did not return a JSON object.")

                merged_result.update(result_json)
                logger.info(f"Successfully extracted schema: {schema_name}")
                break

            except Exception as err:
                attempt += 1
                logger.info(f"Attempt {attempt} failed for schema '{schema_name}': {err}")
                
                if attempt == MAX_RETRIES:
                    logger.error(f"Schema '{schema_name}' failed after {MAX_RETRIES} attempts.")
                    return None
                time.sleep(RETRY_DELAY_SECONDS * attempt)
        
    report_metadata = merged_result.get("report_metadata", {})
    company_legal_name = report_metadata.get("company_legal_name")
    reporting_year = report_metadata.get("reporting_year")

    if not company_legal_name or not reporting_year:
        logger.error("Missing 'company_legal_name' or 'reporting_year' in report metadata.")
        return None
    
    return {
        "_id": company_legal_name,
        "year": str(reporting_year),
        "esg_report": merged_result,
        "token_usage": token_usage
    }

@tool    
def upsert_esg_report(document: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Tool: ESG Report Upserter

    Inserts or updates a specific ESG report for a company in the database.

    This tool:
    - Upserts an ESG report under the `esg_reports.{year}` path in the document.
    - Automatically creates a company document if it doesn't exist.
    - Logs operation type: inserted, updated, unchanged, or error.

    Input:
        document (dict):
            {
                "_id": <company_legal_name>,
                "year": <reporting_year>,
                "esg_report": {structured ESG data}
            }

    Output:
        dict | None:
            {
                "status": "inserted" | "updated" | "unchanged" | "error",
                "company_id": str,
                "year": str,
                "esg_report_keys": list[str] (optional),
                "message": str (on error),
                "missing_keys": list[str] (on error)
            }
    """
    try:
        logger.info(f"Input document: {document}")

        required_keys = {"_id", "year", "esg_report"}
        if not required_keys.issubset(document):
            missing = required_keys - document.keys()
            msg = f"Missing keys in document: {missing}"
            logger.error(msg)
            return {
                "status": "error",
                "message": msg,
                "missing_keys": list(missing)
            }

        company_id = document["_id"]
        year = str(document["year"])
        esg_report_data = document["esg_report"]

        update_path = f"esg_reports.{year}"
        update_doc = { "$set": { update_path: esg_report_data }}

        collection = config.ESG_REPORT_COLLECTION

        result = collection.update_one(
            { "_id": company_id },
            update_doc,
            upsert=True
        )

        if result.upserted_id:
            status = "inserted"
        elif result.modified_count > 0:
            status = "updated"
        else:
            status = "unchanged"

        logger.info(f"ESG report {status} for company_id={company_id}, year={year}")

        return {
            "status": status,
            "company_id": company_id,
            "year": year,
            "esg_report_keys": list(esg_report_data.keys())
        }

    except Exception as e:
        msg = f"Exception during ESG report upsert: {e}"
        logger.error(msg, exc_info=True)
        return {
            "status": "error",
            "message": msg,
            "company_id": document.get("company_id"),
            "year": str(document.get("year", "")),
        }

@tool
def fetch_company_metadata(company_name: str) -> Optional[CompanyMetadata]:
    """
    Tool: Company GICS Classifier

    Uses unstructured web content to classify a company into the GICS taxonomy.

    This tool:
    - Retrieves content via Tavily.
    - Uses OpenAI to classify based on GICS schema.
    - Returns structured metadata (sector, industry, region, etc.).

    Input:
        company_name (str): Name of the company to classify.

    Output:
        CompanyMetadata | None:
            {
                company_name, sector, industry_group, industry,
                sub_industries, headquarters, country, region
            }

    Returns None on classification failure or missing data.
    """
    try:
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
            model=config.OPENAI_PEERS_TOOL_MODEL,
            input=messages,
            text_format=CompanyMetadata,
            temperature=0,
        )
        return completion.output_parsed

    except Exception as e:
        logger.error(f"Error classifying company '{company_name}': {e}", exc_info=True)
        return None

@tool
def get_peer_companies(
    metadata: CompanyMetadata,
    num_country_peers: Optional[int] = None,
    num_region_peers: Optional[int] = None
) -> Dict[str, List[Dict[str, str]]]:
    """
    Tool: Peer Company Finder

    Finds ESG peer companies using GICS classification and geographic metadata.

    This tool:
    - Builds a contextual prompt for OpenAI.
    - Uses structured metadata (sector, country, etc.) to retrieve peer companies.
    - Returns peers grouped by geography (country and region).

    Input:
        metadata (CompanyMetadata): Includes classification and location details.
        num_country_peers (int, optional): Number of peers from the same country (default 5).
        num_region_peers (int, optional): Number of peers from the same region (default 5).

    Output:
        dict:
            {
                "country_peers": [ {name, sector, ...}, ... ],
                "region_peers": [ {name, sector, ...}, ... ]
            }

    Returns empty dict on failure or invalid input.
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
        logger.error("Both peer counts are 0. Defaulting to 5 each.")
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
            model=config.OPENAI_PEERS_TOOL_MODEL,
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

@tool
def get_company_sustainability_report(company: str, year: Optional[int] = None) -> List[str]:
    """
    Tool: Sustainability Report Fetcher

    Searches for publicly available sustainability (ESG) report PDFs for a given company.

    This tool:
    - Uses Tavily web search to find sustainability PDFs.
    - Filters results by year if specified.

    Input:
        company (str): Company name.
        year (int, optional): Year to search for (e.g., 2022).

    Output:
        list[str]: URLs of PDF reports .

    Returns an empty list if no valid URLs are found.
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