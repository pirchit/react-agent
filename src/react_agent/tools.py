"""tools.py ― reusable tools for LangGraph agents.

Includes
--------
• **search** – async web search powered by Tavily  
• **gmail_mcp_action** – async POST helper for a Gmail MCP workflow (e.g. on Pipedream)

Both functions are exported in the `TOOLS` list so LangGraph automatically
registers them.
"""

from __future__ import annotations

import os
from typing import Any, Callable, List, Optional, cast

import httpx
from langchain_tavily import TavilySearch  # type: ignore[import-not-found]

from react_agent.configuration import Configuration

# ─────────────────────────────────────────────────────────────────────────────
# Search tool
# ─────────────────────────────────────────────────────────────────────────────


async def search(query: str) -> Optional[dict[str, Any]]:
    """Run a web search with Tavily and return the JSON response."""
    cfg = Configuration.from_context()
    tavily = TavilySearch(max_results=cfg.max_search_results)
    return cast(dict[str, Any], await tavily.ainvoke({"query": query}))


# ─────────────────────────────────────────────────────────────────────────────
# Gmail MCP tool
# ─────────────────────────────────────────────────────────────────────────────

# Base URL of the Pipedream (or other) workflow that handles Gmail actions.
# Keep the trailing slash OFF. Override in `.env` or your hosting config.
_BASE_MCP_URL = os.getenv(
    "GMAIL_MCP_URL",
    "https://mcp.pipedream.net/f7222a51-6ea5-4c19-baea-66420bcc13b8",
)


async def gmail_mcp_action(action: str, payload: dict | None = None) -> dict[str, Any]:
    """Call the Gmail MCP workflow.

    Parameters
    ----------
    action : str
        e.g. "read", "send", "delete" – your workflow decides what actions exist.
    payload : dict | None
        Any extra data the workflow needs (message_id, subject, body, etc.).

    Returns
    -------
    dict
        The JSON response from the workflow, or {"error": "..."} on failure.
    """
    data = {"action": action, **(payload or {})}

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(_BASE_MCP_URL, json=data)
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


# ─────────────────────────────────────────────────────────────────────────────
# Exported tools for LangGraph
# ─────────────────────────────────────────────────────────────────────────────

TOOLS: List[Callable[..., Any]] = [search, gmail_mcp_action]
