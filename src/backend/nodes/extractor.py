import os
import json
from typing import Optional, Dict, Union, List, BinaryIO, Any
import threading
import time

from dotenv import load_dotenv

from google import genai
from langgraph.prebuilt import create_react_agent

from src.backend.utils.logger import get_logger
from src.backend.services.gemini_service import upload_file, get_gemini_client
from src.backend.services.mongo_db_service import upsert_esg_report
from src.backend.models.esg_schema import (
    ReportMetadata, EnvironmentalEmissionsEnergy, EnvironmentalWaterWaste,
    SocialTrainingAndCSR, SocialWorkforceAndWellBeing,
    GovernanceEthicsAndComplaints, GovernanceStructureAndOpenness, Materiality_Metrics
)
from src.backend.utils.system_prompts import EXTRACTOR_TOOL_PROMPT, EXTRACTOR_AGENT_PROMPT

MODEL = "gemini-2.5-flash-preview-04-17"

RESPONSE_SCHEMA = [
    ReportMetadata,
    EnvironmentalEmissionsEnergy,
    EnvironmentalWaterWaste,
    SocialTrainingAndCSR,
    SocialWorkforceAndWellBeing,
    GovernanceEthicsAndComplaints,
    GovernanceStructureAndOpenness,
    Materiality_Metrics
]

load_dotenv()
logger = get_logger()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("Missing OPENAI_API_KEY in environment.")
    raise EnvironmentError("OPENAI_API_KEY not set")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

thread_local = threading.local()

def extract_emission_data_as_json(file_input: Union[BinaryIO, bytes, str]) -> Optional[Dict[str, Any]]:
    """
    Extracts ESG emission-related data from a PDF using the Gemini API.
    Ensures strict schema-by-schema validation and returns None if any schema fails.
    Successfully extracted data is upserted into MongoDB with reporting metadata.

    Args:
        file_input (Union[BinaryIO, bytes, str]): PDF input (file path, stream, or binary data).

    Returns:
        Optional[Dict[str, Any]]: Success message with link, or None if extraction failed.
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

    merged_result: Dict[str, Any] = {}
    token_usage = {
        "total_prompt_tokens": 0,
        "total_output_tokens": 0,
        "total_tokens": 0
    }
    MAX_RETRIES = 10
    RETRY_DELAY_SECONDS = 60

    for schema in RESPONSE_SCHEMA:
        schema_name = getattr(schema, "__name__", str(schema))
        attempt = 0

        while attempt < MAX_RETRIES:
            try:
                local_client = get_gemini_client() if callable(get_gemini_client) else client

                response = local_client.models.generate_content(
                    model=MODEL,
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
                    # raise ValueError("Invalid JSON type")

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

def initialize_extractor_agent():
    """Initializes and returns the emission data extractor agent."""
    extractor_agent = create_react_agent(
        model="openai:gpt-4o-mini",
        tools=[
            extract_emission_data_as_json,
            upsert_esg_report
        ],
        prompt=EXTRACTOR_AGENT_PROMPT,
        name="extractor_assistant"
    )
    return extractor_agent