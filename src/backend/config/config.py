import os
from dotenv import load_dotenv

from pymongo import MongoClient


load_dotenv()

class Config:
    """
    Central configuration for the application.
    Loads settings from environment variables.
    """

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    # Models
    OPENAI_AGENT_MODEL: str = "gpt-4o-mini"
    OPENAI_SUPERVISOR_MODEL: str = "gpt-4o"
    OPENAI_MODEL = "gpt-4o-mini"
    OPENAI_PEERS_TOOL_MODEL = "gpt-4.1"
    GEMINI_EXTRACTION_MODEL = "gemini-2.5-flash-preview-04-17"

    LANGCHAIN_ORCHESTRATOR_MODEL="gpt-4o"

   # MongoDB
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME")
    ESG_REPORT_COLLECTION_NAME: str = "esg_report_extracts"
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB_NAME]
    ESG_REPORT_COLLECTION = db[ESG_REPORT_COLLECTION_NAME] 

    # Retry Logic
    MAX_RETRIES: int = 3
    RETRY_DELAY_SECONDS: int = 60 

    def __init__(self):
        # Validate that essential keys are set
        if not self.GEMINI_API_KEY or not self.OPENAI_API_KEY or not self.MONGODB_URI:
            raise EnvironmentError(
                "Missing one or more essential environment variables: "
                "GEMINI_API_KEY, OPENAI_API_KEY, MONGODB_URI"
            )


config = Config()
