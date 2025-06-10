import os

from openai import OpenAI, OpenAIError

from src.backend.utils.logger import get_logger

logger = get_logger()

def get_openai_client(api_key: str = None) -> OpenAI:
    """
    Initializes and returns an OpenAI client instance.
    
    Args:
        api_key (str, optional): Your OpenAI API key. If not provided, it uses the OPENAI_API_KEY environment variable.
        
    Returns:
        OpenAI: An instance of the OpenAI client.
    
    Raises:
        ValueError: If no API key is provided or found in environment variables.
        OpenAIError: If the OpenAI client fails to initialize.
    """
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OpenAI API key must be provided or set in the OPENAI_API_KEY environment variable.")
    
    try:
        client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized successfully.")
        return client
    except OpenAIError as e:
        logger.error("Failed to initialize OpenAI client: %s", e)
        raise