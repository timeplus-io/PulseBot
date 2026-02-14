# Web Search Skill

## Overview

The `web_search` skill enables PulseBot to search the web for current information, news, and facts. It supports two search providers:

1. **Brave Search API** - Cloud-based search service (requires API key)
2. **SearXNG** - Self-hosted, privacy-respecting metasearch engine (free, local)

## Configuration

### Provider Selection

Configure the search provider in `config.yaml`:

```yaml
search:
  provider: "searxng"  # or "brave"
  brave_api_key: "${BRAVE_API_KEY:-}"
  searxng_url: "http://searxng:8080"
```

### Using SearXNG (Recommended for Local Development)

SearXNG is a privacy-respecting metasearch engine that aggregates results from multiple search engines without tracking.

**Advantages:**
- ✅ Free and open source
- ✅ No API key required
- ✅ Privacy-focused (no tracking)
- ✅ Runs locally in Docker
- ✅ No rate limits or costs

**Setup:**

1. SearXNG is already included in `docker-compose.yaml`:
   ```yaml
   searxng:
     image: searxng/searxng:latest
     ports:
       - "8080:8080"
     volumes:
       - ./searxng:/etc/searxng
   ```

2. Configure in `config.yaml`:
   ```yaml
   search:
     provider: "searxng"
     searxng_url: "http://searxng:8080"  # Use service name in Docker
   ```

3. Start services:
   ```bash
   docker compose up -d
   ```

4. Verify SearXNG is running:
   ```bash
   curl "http://localhost:8080/search?q=test&format=json"
   ```

### Using Brave Search API

Brave Search provides a commercial search API with generous free tier.

**Advantages:**
- ✅ High-quality search results
- ✅ Free tier: 2,000 queries/month
- ✅ Fast and reliable

**Setup:**

1. Get API key from [Brave Search API](https://brave.com/search/api/)

2. Set environment variable:
   ```bash
   export BRAVE_API_KEY="your-api-key-here"
   ```

3. Configure in `config.yaml`:
   ```yaml
   search:
     provider: "brave"
     brave_api_key: "${BRAVE_API_KEY}"
   ```

## Tool Definition

### `web_search`

Search the web for current information, news, or facts.

**Parameters:**
- `query` (string, required) - The search query
- `count` (integer, optional) - Number of results to return (1-10, default: 5)

**Returns:**
```json
[
  {
    "title": "Result title",
    "url": "https://example.com",
    "description": "Result snippet or description"
  }
]
```

**Example Usage:**

The LLM can invoke this tool when it needs current information:

```
User: "What's the latest news about AI?"
Agent: [Calls web_search with query="latest AI news"]
Tool Result: [List of search results]
Agent: "Here's what I found about the latest AI news..."
```

## Implementation Details

### Architecture

The `WebSearchSkill` class supports multiple providers through a unified interface:

```python
class WebSearchSkill(BaseSkill):
    def __init__(
        self,
        provider: str = "brave",
        api_key: str = "",
        searxng_url: str = "http://localhost:8080"
    ):
        self.provider = provider.lower()
        self.api_key = api_key
        self.searxng_url = searxng_url
    
    async def execute(self, tool_name: str, arguments: dict) -> ToolResult:
        if self.provider == "brave":
            return await self._search_brave(query, count)
        elif self.provider == "searxng":
            return await self._search_searxng(query, count)
```

### Provider-Specific Methods

**Brave Search (`_search_brave`)**:
- Endpoint: `https://api.search.brave.com/res/v1/web/search`
- Authentication: API key via `X-Subscription-Token` header
- Response format: Brave Search API JSON

**SearXNG (`_search_searxng`)**:
- Endpoint: `{searxng_url}/search?format=json`
- Authentication: None required
- Response format: SearXNG JSON API

## Switching Providers

To switch between providers:

1. Update `config.yaml`:
   ```yaml
   search:
     provider: "searxng"  # or "brave"
   ```

2. Rebuild and restart services:
   ```bash
   docker compose build pulsebot-agent pulsebot-api
   docker compose up -d
   ```

## Troubleshooting

### SearXNG Issues

**403 Forbidden on JSON API:**
- Ensure `searxng/settings.yml` has JSON format enabled:
  ```yaml
  search:
    formats:
      - html
      - json
  ```

**Connection refused:**
- Verify SearXNG is running: `docker compose ps searxng`
- Check logs: `docker compose logs searxng`
- Ensure correct URL in config (use service name `searxng:8080` in Docker)

### Brave Search Issues

**"API key not configured" error:**
- Verify `BRAVE_API_KEY` environment variable is set
- Check config.yaml has correct substitution: `${BRAVE_API_KEY}`

**HTTP 401 Unauthorized:**
- Verify API key is valid
- Check you haven't exceeded rate limits

**HTTP 429 Too Many Requests:**
- You've exceeded the free tier limit (2,000 queries/month)
- Consider switching to SearXNG for unlimited local searches

## Best Practices

1. **Use SearXNG for development** - Free, unlimited, and privacy-focused
2. **Use Brave for production** - If you need consistent, high-quality results
3. **Cache results** - Consider implementing caching to reduce API calls
4. **Handle errors gracefully** - Both providers can fail; implement fallback logic
5. **Monitor usage** - Track Brave API usage to avoid hitting rate limits

## Security Considerations

### SearXNG
- Runs locally, no external API calls
- No tracking or data collection
- Configure firewall rules if exposing publicly

### Brave Search
- API key should be kept secret
- Use environment variables, never hardcode
- Rotate keys periodically
- Monitor for unauthorized usage

## Related Documentation

- [Skills System Overview](skills.md)
- [SearXNG Documentation](https://docs.searxng.org/)
- [Brave Search API Docs](https://brave.com/search/api/)
