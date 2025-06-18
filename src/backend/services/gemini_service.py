import os
import re
from typing import Optional, Dict, Union, IO, List, BinaryIO
import requests
import io
from dotenv import load_dotenv

from google import genai
from google.genai import types

from src.backend.utils.logger import get_logger
from src.backend.config.config import config

logger=get_logger()
load_dotenv()

def get_gemini_client(api_key: str = None) -> genai.Client:
    """
    Initializes and returns a Gemini (genai) client instance.

    Args:
        api_key (str, optional): Your Gemini API key. If not provided, it uses the GEMINI_API_KEY environment variable.

    Returns:
        genai.Client: An instance of the Gemini client.

    Raises:
        ValueError: If no API key is provided or found in environment variables.
        GenAIError: If the Gemini client fails to initialize.
    """

    try:
        client = genai.Client(api_key = config.GEMINI_API_KEY)
        logger.info("Gemini (genai) client initialized successfully.")
        return client
    except Exception as e:
        logger.error("Failed to initialize Gemini client: %s", e)
        raise

client = get_gemini_client()

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

def delete_files(file_names: Union[str, List[str]], client) -> None:
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
        is_url = isinstance(file, str) and file.startswith(('http://', 'https://'))

        if not file_name:
            if is_url:
                file_name = os.path.basename(file.split("?")[0]) 
            elif isinstance(file, str):
                file_name = os.path.basename(file)
            elif hasattr(file, "name"):
                file_name = os.path.basename(file.name)
                
        if not file_name or not file_name.strip():
            raise ValueError("file_name must be a non-empty string. Could not infer from input.")

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
            uploaded_file = client.files.upload(file=file_content, config=config)
            logger.info(f"File uploaded successfully to Gemini: {gemini_file_key}")
            return uploaded_file

        if isinstance(file, str):
            if not os.path.isfile(file):
                raise FileNotFoundError(f"Local file '{file}' does not exist.")
            with open(file, "rb") as f:
                uploaded_file = client.files.upload(file=f, config=config)
                logger.info(f"File uploaded successfully to Gemini: {gemini_file_key}")
                return uploaded_file
        
        if hasattr(file, "read"):
            file.seek(0)
            uploaded_file = client.files.upload(file=file, config=config)
            logger.info(f"File uploaded successfully to Gemini: {gemini_file_key}")
            return uploaded_file
        
        uploaded_file = client.files.upload(file=file, config=config)
        logger.info(f"File uploaded successfully to Gemini: {gemini_file_key}")
        return uploaded_file

    except Exception as e:
        logger.error(f"Failed to upload file '{file_name}': {e}")
        raise

# files = get_files()
# deleted_file = delete_files(files)