"""Configuration management for PulseBot."""

import os
import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


def _substitute_env_vars(value: Any) -> Any:
    """Recursively substitute environment variables in config values.
    
    Supports ${VAR_NAME} and ${VAR_NAME:-default} syntax.
    """
    if isinstance(value, str):
        pattern = r'\$\{([^}:]+)(?::-([^}]*))?\}'
        
        def replacer(match: re.Match) -> str:
            var_name = match.group(1)
            default = match.group(2) if match.group(2) is not None else ""
            return os.environ.get(var_name, default)
        
        return re.sub(pattern, replacer, value)
    elif isinstance(value, dict):
        return {k: _substitute_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_substitute_env_vars(v) for v in value]
    return value


class AgentConfig(BaseModel):
    """Agent configuration."""
    name: str = "PulseBot"
    model: str = "claude-sonnet-4-20250514"
    provider: str = "anthropic"
    temperature: float = 0.7
    max_tokens: int = 4096


class TimeplusConfig(BaseModel):
    """Timeplus connection configuration."""
    host: str = "localhost"
    port: int = 8463
    username: str = "default"
    password: str = ""


class ProviderConfig(BaseModel):
    """LLM provider configuration."""
    api_key: str = ""
    default_model: str = ""


class OllamaConfig(BaseModel):
    """Ollama local LLM configuration."""
    enabled: bool = False
    host: str = "http://localhost:11434"
    default_model: str = "llama3"
    timeout_seconds: int = 120


class NvidiaConfig(BaseModel):
    """NVIDIA API configuration."""
    api_key: str = ""
    default_model: str = "moonshotai/kimi-k2.5"
    timeout_seconds: int = 120
    enable_thinking: bool = False





class ProvidersConfig(BaseModel):
    """All LLM providers configuration."""
    anthropic: ProviderConfig = Field(default_factory=ProviderConfig)
    openai: ProviderConfig = Field(default_factory=ProviderConfig)
    openrouter: ProviderConfig = Field(default_factory=ProviderConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    nvidia: NvidiaConfig = Field(default_factory=NvidiaConfig)


class TelegramChannelConfig(BaseModel):
    """Telegram channel configuration."""
    enabled: bool = False
    token: str = ""
    allow_from: list[int] = Field(default_factory=list)  # Telegram user IDs


class WebchatChannelConfig(BaseModel):
    """Webchat channel configuration."""
    enabled: bool = True
    port: int = 8000


class ChannelsConfig(BaseModel):
    """All channels configuration."""
    telegram: TelegramChannelConfig = Field(default_factory=TelegramChannelConfig)
    webchat: WebchatChannelConfig = Field(default_factory=WebchatChannelConfig)


class SkillsConfig(BaseModel):
    """Skills configuration."""
    builtin: list[str] = Field(default_factory=lambda: ["web_search", "file_ops", "shell"])
    custom: list[str] = Field(default_factory=list)


class MCPServerConfig(BaseModel):
    """MCP server configuration."""
    name: str
    transport: str = "stdio"
    command: str | None = None
    args: list[str] = Field(default_factory=list)
    url: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)


class ScheduledTaskConfig(BaseModel):
    """Scheduled task configuration."""
    enabled: bool = False
    interval: str | None = None
    cron: str | None = None
    timezone: str = "UTC"
    actions: list[str] = Field(default_factory=list)


class ScheduledTasksConfig(BaseModel):
    """All scheduled tasks configuration."""
    heartbeat: ScheduledTaskConfig = Field(default_factory=ScheduledTaskConfig)
    daily_summary: ScheduledTaskConfig = Field(default_factory=ScheduledTaskConfig)


class APIConfig(BaseModel):
    """API server configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    format: str = "json"


class MemoryConfig(BaseModel):
    """Memory system configuration."""
    similarity_threshold: float = 0.95  # Threshold for duplicate detection (0.0-1.0)
    enabled: bool = True  # Whether memory system is enabled
    
    # Embedding provider configuration for memory operations
    embedding_provider: str = "openai"  # "openai" or "ollama"
    embedding_model: str = "text-embedding-3-small"
    embedding_api_key: str | None = None  # For OpenAI (optional, falls back to providers.openai.api_key)
    embedding_host: str | None = None  # For Ollama (optional, falls back to providers.ollama.host)
    embedding_dimensions: int | None = None  # Optional: auto-detected if not set
    embedding_timeout_seconds: int = 30  # Timeout for embedding requests


class Config(BaseSettings):
    """Main PulseBot configuration."""
    agent: AgentConfig = Field(default_factory=AgentConfig)
    timeplus: TimeplusConfig = Field(default_factory=TimeplusConfig)
    providers: ProvidersConfig = Field(default_factory=ProvidersConfig)
    channels: ChannelsConfig = Field(default_factory=ChannelsConfig)
    skills: SkillsConfig = Field(default_factory=SkillsConfig)
    mcp_servers: list[MCPServerConfig] = Field(default_factory=list)
    scheduled_tasks: ScheduledTasksConfig = Field(default_factory=ScheduledTasksConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)


def load_config(config_path: str | Path = "config.yaml") -> Config:
    """Load configuration from YAML file with environment variable substitution.
    
    Args:
        config_path: Path to the YAML configuration file.
        
    Returns:
        Loaded and validated Config object.
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        # Return default config if file doesn't exist
        return Config()
    
    with open(config_path) as f:
        raw_config = yaml.safe_load(f)
    
    if raw_config is None:
        return Config()
    
    # Substitute environment variables
    config_data = _substitute_env_vars(raw_config)
    
    return Config(**config_data)


def generate_default_config(path: str | Path = "config.yaml") -> None:
    """Generate a default configuration file.
    
    Args:
        path: Path to write the configuration file.
    """
    default_config = """\
# PulseBot Configuration
# Environment variables can be substituted with ${VAR_NAME} syntax

agent:
  name: "PulseBot"
  model: "claude-sonnet-4-20250514"
  provider: "anthropic"
  temperature: 0.7
  max_tokens: 4096

timeplus:
  host: "${TIMEPLUS_HOST:-localhost}"
  port: 8463
  username: "${TIMEPLUS_USER:-default}"
  password: "${TIMEPLUS_PASSWORD:-}"

providers:
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    default_model: "claude-sonnet-4-20250514"
  
  openai:
    api_key: "${OPENAI_API_KEY}"
    default_model: "gpt-4o"
    embedding_model: "text-embedding-3-small"
  
  ollama:
    enabled: true
    host: "${OLLAMA_HOST:-http://localhost:11434}"
    default_model: "llama3"

  nvidia:
    api_key: "${NVIDIA_API_KEY}"
    default_model: "moonshotai/kimi-k2.5"
    enable_thinking: false

channels:
  telegram:
    enabled: false
    token: "${TELEGRAM_BOT_TOKEN}"
    allow_from: []
  
  webchat:
    enabled: true
    port: 8000

skills:
  builtin:
    - web_search
    - file_ops
    - shell
  
  custom: []

mcp_servers: []

scheduled_tasks:
  heartbeat:
    enabled: true
    interval: "30m"
  
  daily_summary:
    enabled: false
    cron: "0 9 * * *"
    timezone: "UTC"

api:
  host: "0.0.0.0"
  port: 8000
  cors_origins:
    - "http://localhost:3000"

logging:
  level: "INFO"
  format: "json"

memory:
  similarity_threshold: 0.95  # Adjust duplicate detection sensitivity (0.0-1.0)
  enabled: true
  
  # Embedding provider configuration for memory operations
  # Supports "openai" (cloud) or "ollama" (local)
  embedding_provider: "openai"  # or "ollama"
  embedding_model: "text-embedding-3-small"  # OpenAI: text-embedding-3-small (1536), text-embedding-3-large (3072)
                                              # Ollama: mxbai-embed-large (1024), all-minilm (384), nomic-embed-text (768)
  # embedding_api_key: "${OPENAI_API_KEY}"     # Optional: override OpenAI API key
  # embedding_host: "${OLLAMA_HOST}"           # Optional: override Ollama host
  # embedding_dimensions: 1536                 # Optional: auto-detected if not set
  embedding_timeout_seconds: 30
"""
    
    path = Path(path)
    path.write_text(default_config)
