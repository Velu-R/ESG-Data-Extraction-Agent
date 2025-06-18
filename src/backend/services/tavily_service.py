import os
from typing import Literal, Dict, Any

from src.backend.utils.logger import get_logger
from src.backend.config.config import config

logger = get_logger()

def fetch_info_from_tavily(query: str, search_depth: Literal['basic', 'advanced'] = "basic") -> Dict[str, Any]:
    """
    Fetches web-based information related to a natural language query using Tavily's Search API.

    This utility function uses the Tavily `search` endpoint to perform a fast and relevant search
    across the web. It supports answering factual questions, summarizing topics, or retrieving 
    concise information with supporting links.

    Args:
        query (str): A natural language question or phrase, such as 
                     "What does OpenAI do?" or "Where is Microsoft headquartered?".

    Returns:
        Dict[str, Any]: A dictionary that typically includes the following keys:
            - "query" (str): The original query string.
            - "answer" (str, optional): A concise, generated answer summarizing the results.
            - "images" (list, optional): A list of image URLs or metadata (may be empty).
            - "results" (list[dict]): A list of search results. Each result is a dictionary with:
                - "title" (str): The title of the source page.
                - "url" (str): The URL of the result.
                - "content" (str): A short summary or snippet from the page.
                - "score" (float): Relevance score between 0 and 1.
                - "raw_content" (str or None): Full unstructured content if available.
            - "response_time" (str, optional): Time taken to generate the response (in seconds).

        If the query fails or no results are found, the returned dictionary may contain:
            - "error" (str): A descriptive error message.
            - "info" (str): An informational message indicating no results.

    Raises:
        Logs and catches network errors, timeout issues, and any other unexpected exceptions.
    """
    try:
        logger.info("Querying Tavily: '%s'", query)
        tavily_client = config.get_tavily_client()
        response = tavily_client.search(query=query, search_depth=search_depth)

        if not isinstance(response, dict):
            logger.warning("Unexpected response format from Tavily for query '%s': %s", query, response)
            return {"error": f"Unexpected response format for query: '{query}'."}

        results = response.get("results")
        if not results:
            logger.info("No results found for query: '%s'", query)
            return {"info": f"No information found for query: '{query}'."}

        answer = response.get("answer")
        images = response.get("images", [])
        response_time = response.get("response_time")

        logger.info("Retrieved %d result(s) for query '%s'.", len(results), query)
        return {
            "query": query,
            "answer": answer,
            "images": images,
            "results": results,
            "response_time": response_time
        }

    except ConnectionError as ce:
        logger.exception("Network error while querying '%s': %s", query, str(ce))
        return {"error": f"Network issue while retrieving information for query: '{query}'."}

    except TimeoutError as te:
        logger.exception("Timeout error while querying '%s': %s", query, str(te))
        return {"error": f"Request timed out for query: '{query}'."}

    except Exception as e:
        logger.exception("Unexpected error while querying '%s': %s", query, str(e))
        return {"error": f"Unexpected error while retrieving information for query: '{query}'."}
    
# query = f"What does {company_name} do and where it is located"
# response = fetch_info_from_tavily(query=query)
# content = [res.get("content") for res in response['results'] if res.get("content")]