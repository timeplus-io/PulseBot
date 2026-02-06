"""Web search skill using Brave Search API."""

from __future__ import annotations

from typing import Any

import aiohttp

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from pulsebot.utils import get_logger

logger = get_logger(__name__)


class WebSearchSkill(BaseSkill):
    """Web search using Brave Search API.
    
    Example:
        >>> skill = WebSearchSkill(api_key="...")
        >>> result = await skill.execute("web_search", {"query": "weather forecast"})
    """
    
    name = "web_search"
    description = "Search the web for current information"
    
    def __init__(self, api_key: str = ""):
        """Initialize web search skill.
        
        Args:
            api_key: Brave Search API key
        """
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
    
    def get_tools(self) -> list[ToolDefinition]:
        """Return web search tool definition."""
        return [
            ToolDefinition(
                name="web_search",
                description="Search the web for current information, news, or facts. Returns snippets and URLs.",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        },
                        "count": {
                            "type": "integer",
                            "description": "Number of results (1-10)",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            )
        ]
    
    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        """Execute web search.
        
        Args:
            tool_name: Should be "web_search"
            arguments: Search arguments
            
        Returns:
            Search results
        """
        if tool_name != "web_search":
            return ToolResult.fail(f"Unknown tool: {tool_name}")
        
        if not self.api_key:
            return ToolResult.fail("Web search API key not configured")
        
        query = arguments.get("query", "")
        if not query:
            return ToolResult.fail("Search query is required")
        
        count = min(arguments.get("count", 5), 10)
        
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.base_url,
                    headers=headers,
                    params={"q": query, "count": count}
                ) as response:
                    if response.status != 200:
                        return ToolResult.fail(f"Search failed: HTTP {response.status}")
                    
                    data = await response.json()
                    results = []
                    
                    for item in data.get("web", {}).get("results", []):
                        results.append({
                            "title": item.get("title"),
                            "url": item.get("url"),
                            "description": item.get("description"),
                        })
                    
                    logger.debug(f"Web search returned {len(results)} results")
                    
                    return ToolResult.ok(results)
                    
        except aiohttp.ClientError as e:
            return ToolResult.fail(f"Network error: {e}")
        except Exception as e:
            return ToolResult.fail(f"Search error: {e}")
