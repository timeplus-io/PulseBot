"""Web search skill supporting multiple providers."""

from __future__ import annotations

from typing import Any

import aiohttp

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from pulsebot.utils import get_logger

logger = get_logger(__name__)


class WebSearchSkill(BaseSkill):
    """Web search using multiple providers (Brave Search API or SearXNG).
    
    Example:
        >>> # Using Brave Search
        >>> skill = WebSearchSkill(provider="brave", api_key="...")
        >>> result = await skill.execute("web_search", {"query": "weather forecast"})
        
        >>> # Using SearXNG
        >>> skill = WebSearchSkill(provider="searxng", searxng_url="http://localhost:8080")
        >>> result = await skill.execute("web_search", {"query": "weather forecast"})
    """
    
    name = "web_search"
    description = "Search the web for current information"
    
    def __init__(
        self,
        provider: str = "brave",
        api_key: str = "",
        searxng_url: str = "http://localhost:8080"
    ):
        """Initialize web search skill.
        
        Args:
            provider: Search provider - "brave" or "searxng"
            api_key: Brave Search API key (required for brave provider)
            searxng_url: SearXNG instance URL (required for searxng provider)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.searxng_url = searxng_url.rstrip("/")
        
        if self.provider not in ("brave", "searxng"):
            raise ValueError(f"Unsupported provider: {provider}. Use 'brave' or 'searxng'")
    
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
        
        query = arguments.get("query", "")
        if not query:
            return ToolResult.fail("Search query is required")
        
        count = min(arguments.get("count", 5), 10)
        
        # Route to provider-specific method
        if self.provider == "brave":
            return await self._search_brave(query, count)
        elif self.provider == "searxng":
            return await self._search_searxng(query, count)
        else:
            return ToolResult.fail(f"Unsupported provider: {self.provider}")
    
    async def _search_brave(self, query: str, count: int) -> ToolResult:
        """Search using Brave Search API.
        
        Args:
            query: Search query
            count: Number of results
            
        Returns:
            Search results
        """
        if not self.api_key:
            return ToolResult.fail("Brave Search API key not configured")
        
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    headers=headers,
                    params={"q": query, "count": count}
                ) as response:
                    if response.status != 200:
                        return ToolResult.fail(f"Brave Search failed: HTTP {response.status}")
                    
                    data = await response.json()
                    results = []
                    
                    for item in data.get("web", {}).get("results", []):
                        results.append({
                            "title": item.get("title"),
                            "url": item.get("url"),
                            "description": item.get("description"),
                        })
                    
                    logger.debug(f"Brave Search returned {len(results)} results")
                    return ToolResult.ok(results)
                    
        except aiohttp.ClientError as e:
            return ToolResult.fail(f"Network error: {e}")
        except Exception as e:
            return ToolResult.fail(f"Search error: {e}")
    
    async def _search_searxng(self, query: str, count: int) -> ToolResult:
        """Search using SearXNG.
        
        Args:
            query: Search query
            count: Number of results
            
        Returns:
            Search results
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.searxng_url}/search",
                    params={
                        "q": query,
                        "format": "json",
                        "pageno": 1
                    }
                ) as response:
                    if response.status != 200:
                        return ToolResult.fail(f"SearXNG search failed: HTTP {response.status}")
                    
                    data = await response.json()
                    results = []
                    
                    # SearXNG returns results in "results" array
                    for item in data.get("results", [])[:count]:
                        results.append({
                            "title": item.get("title"),
                            "url": item.get("url"),
                            "description": item.get("content", ""),
                        })
                    
                    logger.debug(f"SearXNG returned {len(results)} results")
                    return ToolResult.ok(results)
                    
        except aiohttp.ClientError as e:
            return ToolResult.fail(f"Network error connecting to SearXNG: {e}")
        except Exception as e:
            return ToolResult.fail(f"SearXNG search error: {e}")
