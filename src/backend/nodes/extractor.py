import os
import json
from typing import Optional, Dict, Union, List, BinaryIO, Any

from dotenv import load_dotenv

from google import genai
from langgraph.prebuilt import create_react_agent

# Local imports
from src.backend.utils.logger import get_logger
from src.backend.services.gemini_service import upload_file
from src.backend.models.response_schema import (GEMINI_GHG_PARAMETERS, GEMINI_ENVIRONMENT_PARAMETERS, 
    GEMINI_ENVIRONMENTAL_PARAMETERS_CSRD, GEMINI_GOVERNANCE_PARAMETERS, 
    GEMINI_MATERIALITY_PARAMETERS, GEMINI_NET_ZERO_INTERVENTION_PARAMETERS, GEMINI_SOCIAL_PARAMETERS)
from src.backend.utils.system_prompts import EXTRACTOR_TOOL_PROMPT,EXTRACTOR_SYSTEM_PROMPT

load_dotenv()
logger = get_logger()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("Missing OPENAI_API_KEY in environment.")
    raise EnvironmentError("OPENAI_API_KEY not set")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

RESPONSE_SCHEMA = [ GEMINI_GHG_PARAMETERS, GEMINI_ENVIRONMENT_PARAMETERS,
                    GEMINI_ENVIRONMENTAL_PARAMETERS_CSRD, GEMINI_GOVERNANCE_PARAMETERS, 
                    GEMINI_MATERIALITY_PARAMETERS, GEMINI_NET_ZERO_INTERVENTION_PARAMETERS, GEMINI_SOCIAL_PARAMETERS ]

def extract_emission_data_as_json(file_input: Union[BinaryIO, bytes, str]) -> Optional[Dict[str, Any]]:
    """
    Extracts emission-related ESG data from a PDF file using the Gemini API,
    iterating over all schemas and appending successful results.

    Args:
        file_input (Union[BinaryIO, bytes, str]): Input PDF (file path, binary stream, or file object).

    Returns:
        Optional[Dict]: Dictionary with merged results, raw fallback responses, and token usage summary.
    """
    try:
        logger.info("Uploading file to Gemini.")
        uploaded_file = upload_file(file=file_input)

        all_results: List[Dict[str, Any]] = []
        raw_responses: List[str] = []

        total_prompt_tokens = 0
        total_output_tokens = 0
        total_tokens = 0

        for schema in RESPONSE_SCHEMA:
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=[uploaded_file, EXTRACTOR_TOOL_PROMPT],
                    config={
                        'response_mime_type': 'application/json',
                        'response_schema': schema,
                        'temperature': 0.0,
                    },
                )

                if hasattr(response, 'usage_metadata'):
                    total_prompt_tokens += response.usage_metadata.prompt_token_count or 0
                    total_output_tokens += response.usage_metadata.candidates_token_count or 0
                    total_tokens += response.usage_metadata.total_token_count or 0

                try:
                    parsed = json.loads(response.text)
                    all_results.append(parsed)
                    logger.info("Successfully parsed JSON.")
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON for this schema.")
                    raw_responses.append(response.text)

            except Exception as schema_error:
                logger.warning(f"Error with schema {schema}: {schema_error}")

        if not all_results and not raw_responses:
            logger.error("No data could be extracted.")
            return None

        combined_results = {
            "parsed_results": all_results if all_results else None,
        }

        combined_token_usage = {
            "token_usage": {
                "total_prompt_tokens": total_prompt_tokens,
                "total_output_tokens": total_output_tokens,
                "total_tokens": total_tokens
            }
        }

        logger.info(f"Final token usage: {combined_token_usage['token_usage']}")
        return combined_results

    except Exception as e:
        logger.exception("Unhandled error during ESG data extraction.")
        return None

def initialize_extractor_agent():
    """Initializes and returns the emission data extractor agent."""
    extractor_agent = create_react_agent(
        model="openai:gpt-4o-mini",
        tools=[extract_emission_data_as_json],
        prompt=EXTRACTOR_SYSTEM_PROMPT,
        name="extractor_assistant"
    )
    return extractor_agent