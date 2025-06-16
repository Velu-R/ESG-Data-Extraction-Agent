import os
import json
import threading
import time
from typing import Dict, Any, Union, BinaryIO

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langgraph.types import interrupt
from langchain_core.tools import tool

from google import genai
from pymongo import MongoClient, errors

from src.backend.utils.logger import get_logger
from src.backend.services.gemini_service import upload_file, get_gemini_client
from src.backend.services.mongo_db_service import upsert_esg_report
from src.backend.models.esg_schema import (
    ReportMetadata, EnvironmentalEmissionsEnergy, EnvironmentalWaterWaste,
    SocialWorkforceAndWellBeing,SocialTrainingAndCSR,
    GovernanceEthicsAndComplaints, GovernanceStructureAndOpenness, MaterialityAssessment
)
from src.backend.utils.system_prompts import EXTRACTOR_TOOL_PROMPT, EXTRACTOR_AGENT_PROMPT
from src.backend.utils.state import ExtractorState, AgentState

from src.backend.tools.tool import extract_emission_data_as_json

MODEL = "gemini-2.5-flash-preview-04-17"

RESPONSE_SCHEMA = [
    ReportMetadata,
    # EnvironmentalEmissionsEnergy,
    # EnvironmentalWaterWaste,
    # SocialWorkforceAndWellBeing,
    # SocialTrainingAndCSR,
    # GovernanceEthicsAndComplaints,
    # GovernanceStructureAndOpenness,
    MaterialityAssessment
]

load_dotenv()
logger = get_logger()
thread_local = threading.local()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]
ESG_REPORT_EXTRACTS_COLLECTION = "esg_report_extracts"

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("Missing OPENAI_API_KEY in environment.")
    raise EnvironmentError("OPENAI_API_KEY not set")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# @tool
# def extract_emission_data_as_json(file_input=None, messages=None, **kwargs)  -> Dict[str, Any]:
#     """
#     Extracts ESG emission-related data from a PDF using the Gemini API.
#     Ensures strict schema-by-schema validation and returns None if any schema fails.
#     Successfully extracted data is upserted into MongoDB with reporting metadata.

#     Args:
#         file_input (Union[BinaryIO, bytes, str]): PDF input (file path, stream, or binary data).

#     Returns:
#         Optional[Dict[str, Any]]: Success message with link, or None if extraction failed.
#     """
#     if not file_input:
#         raise interrupt("Missing file input for ESG extraction.")

#     try:
#         uploaded_file = upload_file(file=file_input)
#         if not uploaded_file:
#             raise interrupt("Failed to upload file to Gemini.")
#     except Exception as e:
#         raise interrupt(f"Error during file upload: {e}")

#     merged_result: Dict[str, Any] = {}
#     token_usage = {
#         "total_prompt_tokens": 0,
#         "total_output_tokens": 0,
#         "total_tokens": 0
#     }

#     for schema in RESPONSE_SCHEMA:
#         schema_name = getattr(schema, "__name__", str(schema))
#         attempt = 0
#         MAX_RETRIES = 3
#         RETRY_DELAY_SECONDS = 60

#         while attempt < MAX_RETRIES:
#             try:
#                 local_client = get_gemini_client() if callable(get_gemini_client) else client

#                 response = local_client.models.generate_content(
#                     model=MODEL,
#                     contents=[uploaded_file, EXTRACTOR_TOOL_PROMPT],
#                     config={
#                         'response_mime_type': 'application/json',
#                         'response_schema': schema,
#                         'temperature': 0.0,
#                     },
#                 )

#                 usage = getattr(response, "usage_metadata", None)
#                 if usage:
#                     token_usage["total_prompt_tokens"] += usage.prompt_token_count or 0
#                     token_usage["total_output_tokens"] += usage.candidates_token_count or 0
#                     token_usage["total_tokens"] += usage.total_token_count or 0

#                 raw_text = getattr(response, "text", "")
#                 if not raw_text and getattr(response, "candidates", []):
#                     raw_text = response.candidates[0].content.parts[0].text

#                 if not raw_text:
#                     raise ValueError("Empty response from Gemini")

#                 result_json = json.loads(raw_text)
#                 if not isinstance(result_json, dict):
#                     raise ValueError("Gemini returned non-dict result.")

#                 merged_result.update(result_json)
#                 logger.info(f"Successfully extracted schema: {schema_name}")
#                 break

#             except Exception as err:
#                 attempt += 1
#                 logger.info(f"Attempt {attempt} failed for schema '{schema_name}': {err}")
                
#                 if attempt == MAX_RETRIES:
#                     raise interrupt(f"Failed to extract schema '{schema_name}' after {MAX_RETRIES} retries.")
#                 time.sleep(RETRY_DELAY_SECONDS * attempt)
        
#     report_metadata = merged_result.get("report_metadata", {})
#     company_legal_name = report_metadata.get("company_legal_name")
#     reporting_year = report_metadata.get("reporting_year")

#     if not report_metadata.get("company_legal_name") or not report_metadata.get("reporting_year"):
#         logger.error(f"report_metadata extraction failed: {json.dumps(report_metadata, indent=2)}")
#         raise interrupt("Missing company name or reporting year in metadata.")
    
#     logger.info(f"Merged result: {json.dumps(merged_result, indent=2)}")
#     return {
#         "_id": company_legal_name,
#         "year": str(reporting_year),
#         "esg_report": merged_result,
#         "token_usage": token_usage,
#         "messages": (messages or []) + [{"role": "system", "content": "Extraction succeeded."}],
#         "extraction_status": "success"
#     }

# @tool
# def upsert_esg_report(document: Dict) -> bool:
#     """
#     Upserts a year-specific ESG report into the 'esg_reports.{year}' field of a company document.

#     If the company (_id) exists, the ESG report for the given year is updated. Otherwise,
#     a new document is created. Logs success or error.

#     Args:
#         document (Dict): Must contain '_id', 'year', and 'esg_report'.

#     Returns:
#         Dict[str, Any]: Result including status ('inserted' or 'updated'), message, and identifiers.
#     """
#     try:
#         logger.info(f"Document : {document}")
#         required_keys = {"_id", "year", "esg_report"}
#         if not required_keys.issubset(document):
#             missing = required_keys - document.keys()
#             msg = f"Missing keys in document: {missing}"
#             logger.error(msg)
#             return {"status": "error", "message": msg}

#         company_id = document["_id"]
#         year = str(document["year"])
#         esg_report_data = document["esg_report"]

#         update_path = f"esg_reports.{year}"
#         update_doc = { "$set": { update_path: esg_report_data }}
#         collection = db[ESG_REPORT_EXTRACTS_COLLECTION]

#         result = collection.update_one(
#             { "_id": company_id },
#             update_doc,
#             upsert=True
#         )

#         if result.upserted_id:
#             msg = f"ESG report inserted for company_id={company_id}, year={year}"
#             logger.info(msg)
#             return {
#                 "status": "inserted",
#                 "company_id": company_id,
#                 "year": year,
#                 "message": msg
#             }
        
#         elif result.modified_count > 0:
#             msg = f"ESG report updated for company_id={company_id}, year={year}"
#             logger.info(msg)
#             return {
#                 "status": "updated",
#                 "company_id": company_id,
#                 "year": year,
#                 "message": msg
#             }
        
#         else:
#             msg = f"No changes made to ESG report for company_id={company_id}, year={year}"
#             logger.info(msg)
#             return {
#                 "status": "unchanged",
#                 "company_id": company_id,
#                 "year": year,
#                 "message": msg
#             }
#     except Exception as e:
#         msg = f"Exception during ESG report upsert: {e}"
#         logger.error(msg)
#         return {
#             "status": "error",
#             "company_id": document.get("_id"),
#             "year": str(document.get("year", "")),
#             "message": msg
#         }
    
# @tool
# def extract_emission_data_as_json(state: ExtractorState) -> ExtractorState:
#     """
#     Extracts ESG emission-related data from a PDF using the Gemini API.
#     Ensures strict schema-by-schema validation and returns None if any schema fails.
#     Successfully extracted data is upserted into MongoDB with reporting metadata.

#     Args:
#         file_input (Union[BinaryIO, bytes, str]): PDF input (file path, stream, or binary data).

#     Returns:
#         Optional[Dict[str, Any]]: Success message with link, or None if extraction failed.
#     """
#     state = dict(state or {})
#     file_input = state.get("file_input")
#     messages = state.get("messages", [])

#     if not file_input:
#         raise interrupt("Missing file input for ESG extraction.")

#     try:
#         uploaded_file = upload_file(file=file_input)
#         if not uploaded_file:
#             raise interrupt("Failed to upload file to Gemini.")
#     except Exception as e:
#         raise interrupt(f"Error during file upload: {e}")

#     merged_result = {}
#     token_usage = {"total_prompt_tokens": 0, "total_output_tokens": 0, "total_tokens": 0}

#     for schema in RESPONSE_SCHEMA:
#         schema_name = getattr(schema, "__name__", str(schema))
#         for attempt in range(3):
#             try:
#                 gemini = get_gemini_client() if callable(get_gemini_client) else gemini_client
#                 response = gemini.models.generate_content(
#                     model=MODEL,
#                     contents=[uploaded_file, EXTRACTOR_TOOL_PROMPT],
#                     config={
#                         'response_mime_type': 'application/json',
#                         'response_schema': schema,
#                         'temperature': 0.0,
#                     },
#                 )
#                 usage = getattr(response, "usage_metadata", None)
#                 if usage:
#                     token_usage["total_prompt_tokens"] += usage.prompt_token_count or 0
#                     token_usage["total_output_tokens"] += usage.candidates_token_count or 0
#                     token_usage["total_tokens"] += usage.total_token_count or 0

#                 raw_text = getattr(response, "text", "")
#                 if not raw_text and getattr(response, "candidates", []):
#                     raw_text = response.candidates[0].content.parts[0].text

#                 if not raw_text:
#                     raise ValueError("Empty response from Gemini")

#                 result_json = json.loads(raw_text)
#                 if not isinstance(result_json, dict):
#                     raise ValueError("Gemini returned non-dict result.")

#                 merged_result.update(result_json)
#                 logger.info(f"Successfully extracted schema: {schema_name}")
#                 break
#             except Exception as err:
#                 logger.warning(f"Attempt {attempt+1} failed for schema '{schema_name}': {err}")
#                 time.sleep(60 * (attempt + 1))
#         else:
#             raise interrupt(f"Failed to extract schema '{schema_name}' after 3 retries.")

#     report_metadata = merged_result.get("report_metadata", {})
#     if not report_metadata.get("company_legal_name") or not report_metadata.get("reporting_year"):
#         logger.error(f"Invalid report_metadata: {json.dumps(report_metadata, indent=2)}")
#         raise interrupt("Missing company name or reporting year in metadata.")
#     logger.info(f"Merged ESG result: {json.dumps(merged_result, indent=2)}")


#     state["company_id"] = report_metadata["company_legal_name"]
#     state['year']= str(report_metadata["reporting_year"])
#     state["esg_report"]= merged_result
#     state["token_usage"]= token_usage
#     state["messages"] = messages + [{"role": "system", "content": "Extraction succeeded."}]
#     state["extraction_status"]= "success"

#     return state

# @tool
# def upsert_esg_report(state: ExtractorState) -> ExtractorState:
#     """
#     Upserts a year-specific ESG report into the 'esg_reports.{year}' field of a company document.

#     If the company (_id) exists, the ESG report for the given year is updated. Otherwise,
#     a new document is created. Logs success or error.

#     Args:
#         document (Dict): Must contain '_id', 'year', and 'esg_report'.

#     Returns:
#         Dict[str, Any]: Result including status ('inserted' or 'updated'), message, and identifiers.
#     """
#     try:
#         logger.info(f"Document : {state}")
#         required_keys = {"company_id", "year", "esg_report"}
#         if not required_keys.issubset(state):
#             missing = required_keys - state.keys()
#             msg = f"Missing keys in document: {missing}"
#             logger.error(msg)
#             return {"status": "error", "message": msg}

#         company_id = state["company_id"]
#         year = str(state["year"])
#         esg_report_data = state["esg_report"]

#         update_path = f"esg_reports.{year}"
#         update_doc = { "$set": { update_path: esg_report_data }}
#         collection = db[ESG_REPORT_EXTRACTS_COLLECTION]

#         result = collection.update_one(
#             { "_id": company_id },
#             update_doc,
#             upsert=True
#         )

#         if result.upserted_id:
#             status = "inserted"
#         elif result.modified_count > 0:
#             status = "updated"
#         else:
#             status = "unchanged"

#         logger.info(f"ESG report {status} for company_id={company_id}, year={year}")
#         state["db_status"] = status
#         return state
    
#     except Exception as e:
#         msg = f"Exception during ESG report upsert: {e}"
#         logger.error(msg)
#         return {
#             "status": "error",
#             "company_id": state.get("company_id"),
#             "year": str(state.get("year", "")),
#             "message": msg
#         }

def initialize_extractor_agent():
    """Initializes and returns the emission data extractor agent."""
    extractor_agent = create_react_agent(
        model="openai:gpt-4o-mini",
        tools=[
            extract_emission_data_as_json,
            upsert_esg_report
        ],
        prompt=EXTRACTOR_AGENT_PROMPT,
        name="extractor_assistant",
        state_schema=AgentState
    )
    return extractor_agent