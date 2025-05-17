import os
import re
from typing import Optional, Dict, Union, IO, List, BinaryIO
import requests
import io
from dotenv import load_dotenv

from google import genai
from google.genai import types

from src.backend.utils.logger import get_logger

logger=get_logger()
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT = (
    """You are a PDF parsing agent specialized in extracting structured sustainability data from a company's Sustainability, ESG, or Corporate Responsibility Report in PDF format. 
    Your task is to extract Greenhouse Gas (GHG) Protocol, Environmental (CSRD), Materiality, Net Zero Interventions, and ESG (Environmental, Social, Governance) Data with high accuracy and consistency for downstream processing.

    ### Instructions:
    1. **Schema Adherence**: Strictly follow the provided schema for output structure. Ensure every field in the schema is populated with either extracted data or a placeholder.
    2. **Data Sources**: Extract data from all relevant sections of the PDF, including:
       - Narrative text
       - Tables
       - Infographics, charts, or visual elements (interpret labels, captions, or legends to extract numerical or textual data)
       - Footnotes or appendices
    3. **Infographic Handling**: For infographics, prioritize:
       - Text labels or annotations within the graphic
       - Captions or descriptions near the infographic
       - Legends or keys that clarify values
       - If values are ambiguous, cross-reference with narrative text or tables discussing similar metrics.
    4. **Year and Scope**: Identify the reporting year and scope (e.g., global, regional) for each metric. If not explicitly stated, infer from the report's context (e.g., '2023 Sustainability Report' implies 2023 data).
    5. **Edge Cases**:
       - If data is missing, use placeholders as specified in the schema.
       - If multiple values exist for a field (e.g., emissions for different years), select the most recent year unless otherwise specified in the schema.

    ### Output Requirements:
    - Return a JSON object adhering to the schema.
    - Ensure all fields are populated, using placeholders for missing data.
    - Include a 'notes' field in the output for any assumptions, estimations, or conflicts encountered during extraction.


    ### Task:
    - Parse the PDF thoroughly to extract all relevant data.
    - Ensure consistency in units, years, and terminology across the output.
    - Handle infographics with care, prioritizing textual data and flagging estimates.
    - Provide a complete, schema-compliant JSON output with notes for any ambiguities or assumptions.
    """
)

def sanitize_file_name(name: str, max_length: int = 40) -> str:
    """
    Sanitizes a file name to comply with Gemini API naming rules:
    - Lowercase only
    - Alphanumeric characters and dashes (`-`) allowed
    - Cannot start or end with a dash
    - Max length: 40 characters

    Args:
        name (str): The original file name (without extension).
        max_length (int, optional): Maximum allowed characters (default: 40).

    Returns:
        str: Sanitized file name.

    Raises:
        ValueError: If the sanitized name is empty after cleaning.
    """
    if not name or not isinstance(name, str):
        raise ValueError("Invalid file name: must be a non-empty string.")

    name = re.sub(r'[^a-z0-9]+', '-', name.lower())

    name = name.strip('-')[:max_length].rstrip('-')

    if not name:
        raise ValueError("Sanitized file name is empty or invalid after cleanup.")

    return name

def get_files() -> List[str]:
    """
    Retrieves all uploaded file names from Gemini.

    Returns:
        List[str]: List of existing file names.
    """
    files = client.files.list()
    return [file.name for file in files]

def delete_files(file_names: Union[str, List[str]]) -> None:
    """
    Deletes specified files from Gemini.

    Args:
        file_names (Union[str, List[str]]): File name or list of names to delete.
    """
    if not file_names:
        logger.info("No file names provided for deletion.")
        return

    if isinstance(file_names, str):
        file_names = [file_names]

    existing_files = get_files()

    for name in file_names:
        logger.info(f"Attempting to delete file: {name}")
        if name in existing_files:
            client.files.delete(name=name)
            logger.info(f"Deleted file: {name}")
        else:
            logger.error(f"File not found: {name}")

def upload_file(
    file: Union[BinaryIO, bytes, str, IO[bytes]],
    file_name: Optional[str] = None,
    config: Optional[Dict[str, str]] = None
) -> Optional[types.File]:
    """
    Uploads a file to the Gemini API, handling local file paths, binary streams, and URLs.

    Args:
        file (Union[BinaryIO, bytes, str, IO[bytes]]): Local file path, URL, or binary file object.
        file_name (Optional[str]): Name for the file. If None, tries to infer it from the source.
        config (Optional[Dict[str, str]]): Extra config like 'mime_type'.

    Returns:
        Optional[types.File]: The uploaded Gemini file object, or existing one if already uploaded.

    Raises:
        Exception: If upload fails.
    """
    try:
        logger.info(f"Uploading file: {file}")
        is_url = isinstance(file, str) and file.startswith(('http://', 'https://'))

        if not file_name:
            if is_url:
                file_name = os.path.basename(file.split("?")[0]) 
            elif isinstance(file, str):
                file_name = os.path.basename(file)
            elif hasattr(file, "name"):
                file_name = os.path.basename(file.name)
            else:
                raise ValueError("file_name must be provided if file has no 'name' attribute.")

        sanitized_name = sanitize_file_name(os.path.splitext(file_name)[0])
        mime_type = "application/pdf"
        config = config or {}
        config.update({"name": sanitized_name, "mime_type": mime_type})
        gemini_file_key = f"files/{sanitized_name}"

        if gemini_file_key in get_files():
            logger.info(f"File already exists on Gemini: {gemini_file_key}")
            return client.files.get(name=gemini_file_key)

        logger.info(f"Uploading file to Gemini: {gemini_file_key}")

        if is_url:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.get(file, headers=headers)
            response.raise_for_status()
            file_content = io.BytesIO(response.content)
            return client.files.upload(file=file_content, config=config)

        if isinstance(file, str):
            if not os.path.isfile(file):
                raise FileNotFoundError(f"Local file '{file}' does not exist.")
            with open(file, "rb") as f:
                return client.files.upload(file=f, config=config)
        
        if hasattr(file, "read"):
            file.seek(0)
            return client.files.upload(file=file, config=config)

        return client.files.upload(file=file, config=config)

    except Exception as e:
        logger.error(f"Failed to upload file '{file_name}': {e}")
        raise

# files = get_files()
# deleted_file = delete_files(files)