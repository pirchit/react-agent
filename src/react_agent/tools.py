"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast
import requests  # Add this import at the top with the others

from langchain_tavily import TavilySearch  # type: ignore[import-not-found]

from react_agent.configuration import Configuration


async def search(query: str) -> Optional[dict[str, Any]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_context()
    wrapped = TavilySearch(max_results=configuration.max_search_results)
    return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))


async def gmail_mcp_action(action: str, payload: dict = None) -> dict:
    """
    Interact with the Gmail MCP server.

    Args:
        action (str): The action to perform (e.g., 'send', 'read', 'delete').
        payload (dict, optional): The data to send with the request.

    Returns:
        dict: The response from the MCP server.
    """
    url = f"https://mcp.pipedream.net/f7222a51-6ea5-4c19-baea-66420bcc13b8/gmail/{action}"
    try:
        response = requests.post(url, json=payload or {})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


TOOLS: List[Callable[..., Any]] = [search, gmail_mcp_action]
