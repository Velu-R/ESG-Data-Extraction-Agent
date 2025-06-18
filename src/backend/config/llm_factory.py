import os
from typing import Literal, Union
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from src.backend.config.config import config


class LLMFactory:
    """
    Factory class to return a LangChain LLM instance based on the provider.
    Currently supports 'openai' and 'gemini'.
    """

    def __init__(self, provider: Literal["openai", "gemini"] = "openai"):
        self.llm = self.get_llm(provider)

    @staticmethod
    def get_llm(provider: Literal["openai", "gemini"] = "openai") -> Union[ChatOpenAI, ChatGoogleGenerativeAI]:
        """
        Returns an LLM client instance based on the provider.

        Args:
            provider (Literal["openai", "gemini"]): The LLM provider to use.

        Returns:
            A LangChain LLM instance.

        Raises:
            ValueError: If the specified provider is not supported.
        """
        if provider == "openai":
            return config.get_openai_client()
        elif provider == "gemini":
            return config.get_gemini_client()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
