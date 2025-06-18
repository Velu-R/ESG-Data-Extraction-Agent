import os
from typing import Optional

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient


load_dotenv()

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

class Config:
    """
    Loads values from environment variables and provides clients as needed.
    """
    # === Environment Variables ===
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY: Optional[str] = os.getenv("TAVILY_API_KEY") 

    MONGODB_URI: str = os.getenv("MONGODB_URI")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "esg_db")
    ESG_REPORT_COLLECTION_NAME: str = os.getenv("ESG_REPORT_COLLECTION_NAME", "esg_report_extracts")

    # === Model Names ===
    OPENAI_PEERS_TOOL_MODEL: str = os.getenv("OPENAI_PEERS_TOOL_MODEL", "gpt-4.1")
    GEMINI_EXTRACTION_MODEL: str = os.getenv("GEMINI_EXTRACTION_MODEL", "gemini-2.5-flash-preview-04-17")
    LANGCHAIN_ORCHESTRATOR_MODEL: str = os.getenv("LANGCHAIN_ORCHESTRATOR_MODEL", "gpt-4o")

    # === Retry Logic ===
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", 3))
    RETRY_DELAY_SECONDS: int = int(os.getenv("RETRY_DELAY_SECONDS", 60))

    def __init__(self):
        self._validate_essentials()
        self._mongo_client: MongoClient = MongoClient(self.MONGODB_URI)
        self._mongo_db: Database = self._mongo_client[self.MONGODB_DB_NAME]
        self._esg_collection: Collection = self._mongo_db[self.ESG_REPORT_COLLECTION_NAME]

    def _validate_essentials(self) -> None:
        """Validates required environment variables."""
        missing_vars = []
        for var in ["GEMINI_API_KEY", "OPENAI_API_KEY", "MONGODB_URI"]:
            if not getattr(self, var):
                missing_vars.append(var)
        if missing_vars:
            raise ConfigError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        
    @property
    def mongo_client(self) -> MongoClient:
        return self._mongo_client

    @property
    def mongo_db(self) -> Database:
        return self._mongo_db

    @property
    def ESG_REPORT_COLLECTION(self) -> Collection:
        return self._esg_collection

    def get_openai_client(self) -> ChatOpenAI:
        """
        Creates a configured OpenAI client using the global config.

        Returns:
            ChatOpenAI: OpenAI client instance.
        """
        return ChatOpenAI(
            api_key=self.OPENAI_API_KEY,
            model=self.LANGCHAIN_ORCHESTRATOR_MODEL
        )
    
    def get_gemini_client(self) -> ChatGoogleGenerativeAI:
        """
        Creates a configured Gemini (Google Generative AI) client.

        Returns:
            ChatGoogleGenerativeAI: Gemini client instance.
        """
        return ChatGoogleGenerativeAI(
            model=self.GEMINI_EXTRACTION_MODEL,
            google_api_key=self.GEMINI_API_KEY
        )
    
    def get_tavily_client(self) -> TavilyClient:
        """
        Creates a configured Tavily client using the global config.

        Returns:
            TavilyClient: Tavily client instance.
        """
        return TavilyClient(api_key=self.TAVILY_API_KEY)

config = Config()