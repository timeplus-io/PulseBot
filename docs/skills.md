# PulseBot Skills System

## Overview

PulseBot's skills system provides a flexible framework for extending the agent's capabilities through tools. Skills are modular components that the LLM can invoke to perform actions like web searches, file operations, shell commands, or custom integrations.

The skills architecture follows these key principles:
- **OpenAI-Compatible Tool Format**: Skills define tools using the same schema format as OpenAI's function calling API
- **Async Execution**: All skill methods are async for non-blocking I/O operations
- **Dynamic Loading**: Skills can be loaded dynamically from configuration
- **Type Safety**: Uses Pydantic models for validation and type safety
- **Composability**: A skill can expose multiple related tools

## Architecture

### Core Components

```
pulsebot/skills/
├── base.py          # Base classes and models
├── loader.py        # Dynamic skill loading
├── __init__.py
└── builtin/         # Built-in skill implementations
    ├── __init__.py
    ├── web_search.py
    ├── file_ops.py
    └── shell.py
```

### Base Classes

#### `BaseSkill` (Abstract Base Class)

All skills must inherit from `BaseSkill` and implement two abstract methods:

```python
from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult

class MySkill(BaseSkill):
    name = "my_skill"
    description = "Description of what this skill does"
    
    def get_tools(self) -> list[ToolDefinition]:
        """Return list of tools provided by this skill."""
        pass
    
    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        """Execute a tool with given arguments."""
        pass
```

#### `ToolDefinition` (Pydantic Model)

Defines a tool using OpenAI-compatible JSON Schema format:

```python
class ToolDefinition(BaseModel):
    name: str                    # Tool name (must be unique across all skills)
    description: str             # Description for LLM to understand when to use it
    parameters: dict[str, Any]   # JSON Schema for tool arguments
    
    def to_openai_format(self) -> dict[str, Any]:
        """Convert to OpenAI tool format."""
```

#### `ToolResult` (Pydantic Model)

Standardized result format for tool execution:

```python
class ToolResult(BaseModel):
    success: bool           # Whether execution succeeded
    output: Any             # Result data (any JSON-serializable type)
    error: str | None       # Error message if failed
    
    @classmethod
    def ok(cls, output: Any) -> "ToolResult":
        """Create a successful result."""
    
    @classmethod
    def fail(cls, error: str) -> "ToolResult":
        """Create a failed result."""
```

## How Skills Work

### 1. Skill Discovery

The `SkillLoader` manages skill registration and tool discovery:

```python
from pulsebot.skills.loader import SkillLoader

loader = SkillLoader()
loader.load_builtin("web_search", api_key="...")
loader.load_custom("my_project.skills.custom_skill.MyCustomSkill")

# Get all tools for LLM
tools = loader.get_tools()
tools_openai_format = loader.get_tool_definitions()
```

### 2. Tool Execution

When the LLM requests a tool call, the agent:

1. Receives tool name and arguments from LLM
2. Looks up the skill that provides the tool via `SkillLoader.get_skill_for_tool()`
3. Calls `skill.execute(tool_name, arguments)`
4. Returns `ToolResult` to the LLM as a tool result message

### 3. Execution Flow

```
User Message → Agent
                    ↓
            LLM with Tools
                    ↓
            Tool Call Request
                    ↓
            Skill.execute()
                    ↓
            ToolResult → LLM → Final Response
```

## Built-in Skills

### Web Search (`web_search`)

Uses Brave Search API to search the web.

**Tool**: `web_search`
- **Parameters**: `query` (string), `count` (integer, 1-10)
- **Returns**: List of search results with title, URL, and description

**Configuration**:
```yaml
skills:
  builtin:
    - web_search
```

**Environment Variable**: `BRAVE_API_KEY` or pass `api_key` to constructor

### File Operations (`file_ops`)

Read, write, and list files with security guardrails.

**Tools**:
- `read_file`: Read file contents
  - Parameters: `path` (string)
  - Returns: File content as string

- `write_file`: Write content to file
  - Parameters: `path` (string), `content` (string), `append` (boolean)
  - Returns: Bytes written

- `list_directory`: List directory contents
  - Parameters: `path` (string, optional)
  - Returns: List of files with type and size

**Configuration**:
```yaml
skills:
  builtin:
    - file_ops
```

**Constructor Options**:
```python
FileOpsSkill(
    base_path="/allowed/directory",  # Restricts file operations
    allowed_extensions=[".txt", ".py", ".md"]  # Optional extension filter
)
```

### Shell Commands (`shell`)

Execute shell commands with safety controls.

**Tool**: `run_command`
- **Parameters**: `command` (string)
- **Returns**: Exit code, stdout, stderr

**Safety Features**:
- Blocked commands list: `rm`, `rmdir`, `mv`, `sudo`, etc.
- Dangerous pattern detection
- Optional whitelist mode
- Timeout protection (default 30s)
- Output size limits

**Configuration**:
```yaml
skills:
  builtin:
    - shell
```

**Constructor Options**:
```python
ShellSkill(
    allowed_commands=["ls", "cat", "grep"],  # Whitelist mode
    working_directory="/path",  # Working directory
    timeout_seconds=30,
    max_output_length=10000
)
```

## Creating Custom Skills

### Step 1: Create Skill Class

Create a new file, e.g., `my_project/skills/weather_skill.py`:

```python
"""Weather lookup skill using a weather API."""

from __future__ import annotations

from typing import Any

import aiohttp

from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from pulsebot.utils import get_logger

logger = get_logger(__name__)


class WeatherSkill(BaseSkill):
    """Weather lookup skill using OpenWeatherMap API."""
    
    name = "weather"
    description = "Get current weather and forecasts"
    
    def __init__(self, api_key: str = ""):
        """Initialize weather skill.
        
        Args:
            api_key: OpenWeatherMap API key
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_tools(self) -> list[ToolDefinition]:
        """Return weather tool definitions."""
        return [
            ToolDefinition(
                name="get_current_weather",
                description="Get current weather for a city",
                parameters={
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name (e.g., 'San Francisco')"
                        },
                        "units": {
                            "type": "string",
                            "enum": ["metric", "imperial"],
                            "description": "Temperature units",
                            "default": "metric"
                        }
                    },
                    "required": ["city"]
                }
            ),
            ToolDefinition(
                name="get_forecast",
                description="Get 5-day weather forecast",
                parameters={
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name"
                        },
                        "days": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 5,
                            "description": "Number of days",
                            "default": 3
                        }
                    },
                    "required": ["city"]
                }
            )
        ]
    
    async def execute(
        self, 
        tool_name: str, 
        arguments: dict[str, Any]
    ) -> ToolResult:
        """Execute weather tool."""
        if tool_name == "get_current_weather":
            return await self._get_current_weather(arguments)
        elif tool_name == "get_forecast":
            return await self._get_forecast(arguments)
        else:
            return ToolResult.fail(f"Unknown tool: {tool_name}")
    
    async def _get_current_weather(
        self, 
        arguments: dict[str, Any]
    ) -> ToolResult:
        """Fetch current weather."""
        city = arguments.get("city", "")
        units = arguments.get("units", "metric")
        
        if not self.api_key:
            return ToolResult.fail("Weather API key not configured")
        
        if not city:
            return ToolResult.fail("City is required")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/weather"
                params = {
                    "q": city,
                    "appid": self.api_key,
                    "units": units
                }
                
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        return ToolResult.fail(
                            f"Weather API error: HTTP {response.status}"
                        )
                    
                    data = await response.json()
                    result = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"]
                    }
                    return ToolResult.ok(result)
        
        except aiohttp.ClientError as e:
            return ToolResult.fail(f"Network error: {e}")
        except Exception as e:
            return ToolResult.fail(f"Weather lookup failed: {e}")
    
    async def _get_forecast(
        self, 
        arguments: dict[str, Any]
    ) -> ToolResult:
        """Fetch weather forecast."""
        # Implementation similar to _get_current_weather
        pass
```

### Step 2: Register in Config

Add to `config.yaml`:

```yaml
skills:
  builtin:
    - web_search
    - file_ops
    - shell
  custom:
    - my_project.skills.weather_skill.WeatherSkill
```

Or use the `SkillLoader` directly:

```python
from pulsebot.skills.loader import SkillLoader

loader = SkillLoader()
loader.load_custom(
    "my_project.skills.weather_skill.WeatherSkill",
    api_key="your-api-key"
)
```

### Step 3: Best Practices

1. **Input Validation**: Always validate arguments before processing
2. **Error Handling**: Return descriptive errors via `ToolResult.fail()`
3. **Security**: Validate paths, commands, and external inputs
4. **Timeouts**: Use `asyncio.wait_for()` for external API calls
5. **Logging**: Use `get_logger(__name__)` for consistent logging
6. **Documentation**: Write clear descriptions for tools and parameters

### Tool Naming Conventions

- Use descriptive, action-oriented names: `get_weather`, `run_command`, `read_file`
- Avoid generic names that might conflict: use `search_web` instead of `search`
- Use snake_case for consistency with Python conventions

### Parameter Schema Best Practices

```python
ToolDefinition(
    name="my_tool",
    description="Clear, LLM-friendly description of what this does",
    parameters={
        "type": "object",
        "properties": {
            "required_param": {
                "type": "string",
                "description": "What this parameter is for"
            },
            "optional_param": {
                "type": "integer",
                "description": "Description with constraints",
                "minimum": 1,
                "maximum": 100,
                "default": 10
            },
            "enum_param": {
                "type": "string",
                "enum": ["option1", "option2", "option3"],
                "description": "Must be one of the allowed values",
                "default": "option1"
            }
        },
        "required": ["required_param"]  # List required fields
    }
)
```

## Advanced Topics

### Custom Skill Packages

For reusable skills, create a Python package:

```
my_pulsebot_skills/
├── __init__.py
├── weather/
│   ├── __init__.py
│   └── weather_skill.py
├── database/
│   ├── __init__.py
│   └── db_skill.py
└── utils.py
```

Install with pip:
```bash
pip install -e ./my_pulsebot_skills
```

Then reference in config:
```yaml
skills:
  custom:
    - my_pulsebot_skills.weather.WeatherSkill
    - my_pulsebot_skills.database.DatabaseSkill
```

### Skill Composition

Skills can use other skills or shared utilities:

```python
from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult
from my_project.utils import shared_api_client

class ComposedSkill(BaseSkill):
    def __init__(self):
        self.api_client = shared_api_client
        self.cache = {}
    
    async def execute(self, tool_name: str, arguments: dict) -> ToolResult:
        # Use shared resources
        pass
```

### Testing Skills

```python
import pytest
from pulsebot.skills.builtin.web_search import WebSearchSkill

@pytest.fixture
def skill():
    return WebSearchSkill(api_key="test-key")

@pytest.mark.asyncio
async def test_web_search_success(skill, mock_aiohttp):
    # Mock the API response
    mock_aiohttp.get("https://api.search.brave.com/res/v1/web/search", json={
        "web": {"results": [{"title": "Test", "url": "http://test.com"}]}
    })
    
    result = await skill.execute("web_search", {"query": "test"})
    
    assert result.success is True
    assert len(result.output) > 0

@pytest.mark.asyncio
async def test_web_search_no_api_key():
    skill = WebSearchSkill(api_key="")
    result = await skill.execute("web_search", {"query": "test"})
    
    assert result.success is False
    assert "API key" in result.error
```

## Configuration Reference

### SkillsConfig (config.py)

```python
class SkillsConfig(BaseModel):
    builtin: list[str] = ["web_search", "file_ops", "shell"]
    custom: list[str] = []  # Module paths to custom skill classes
```

### Environment Variables

Skills can receive configuration via:

1. **Config YAML**: Per-skill config under `skills:`
2. **Environment Variables**: Standard `${VAR_NAME}` substitution
3. **Constructor Args**: Passed when loading via code

Example with environment variables:

```yaml
skills:
  builtin:
    - web_search
  custom:
    - my_project.skills.weather.WeatherSkill

# In your skill
class WeatherSkill(BaseSkill):
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or os.environ.get("WEATHER_API_KEY", "")
```

## Troubleshooting

### Common Issues

**"Unknown built-in skill" error**:
- Check that the skill name is in the `BUILTIN_SKILLS` registry in `loader.py`
- Verify the module path is correct

**"Failed to load custom skill" error**:
- Ensure the module path is importable (in Python path)
- Verify the class exists and is properly named
- Check for import errors in the skill module

**Tool not being called by LLM**:
- Check tool description is clear and specific
- Ensure parameters schema is correct
- Verify tool name is unique across all skills

**Skill executes but returns errors**:
- Check argument validation
- Verify external dependencies (API keys, network access)
- Review error messages in `ToolResult.fail()` calls

## Summary

The PulseBot skills system provides:

1. **Modularity**: Skills are self-contained and composable
2. **Safety**: Built-in validation and security controls
3. **Flexibility**: Support for both built-in and custom skills
4. **Standards**: OpenAI-compatible tool format
5. **Observability**: All tool calls logged to streams

To add new capabilities to your agent, simply create a skill class, register it in config, and the LLM will automatically be able to invoke it when appropriate.
