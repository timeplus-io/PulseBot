"""WorkspaceConfig — shared configuration model for the Agent Workspace feature.

Consumed by:
  - pulsebot/workspace/manager.py
  - pulsebot/workspace/server.py
  - pulsebot/workspace/registry_client.py
  - pulsebot/workspace/proxy_registry.py
  - pulsebot/workspace/registration_router.py
  - pulsebot/skills/builtin/workspace.py

Values are populated in priority order:
  1. Explicitly passed kwargs (from config.yaml via the Config class)
  2. Environment variables (mapped below — no prefix required)
  3. Field defaults

Env var mapping:
  base_dir          ← WORKSPACE_DIR
  workspace_port    ← WORKSPACE_PORT
  agent_host        ← AGENT_HOST
  api_server_url    ← API_SERVER_URL
  internal_api_key  ← WORKSPACE_INTERNAL_KEY
"""

import os

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

class WorkspaceConfig(BaseSettings):
    model_config = {"extra": "ignore", "populate_by_name": True}

    base_dir: str = Field(default="./workspaces", validation_alias=AliasChoices("base_dir", "WORKSPACE_DIR"))
    workspace_port: int = Field(default=8001, validation_alias=AliasChoices("workspace_port", "WORKSPACE_PORT"))
    agent_host: str = Field(default="localhost", validation_alias=AliasChoices("agent_host", "AGENT_HOST"))
    api_server_url: str = Field(default="http://localhost:8000", validation_alias=AliasChoices("api_server_url", "API_SERVER_URL"))
    backend_boot_timeout: float = Field(default=3.0)
    internal_api_key: str = Field(default="", validation_alias=AliasChoices("internal_api_key", "WORKSPACE_INTERNAL_KEY"))

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        **kwargs,  # ← absorbs secrets_settings, file_secret_settings, etc.
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # env wins over init (YAML kwargs)
        return (env_settings, init_settings, dotenv_settings)

    @property
    def agent_base_url(self) -> str:
        host = os.environ.get("AGENT_HOST") or self.agent_host
        port = os.environ.get("WORKSPACE_PORT") or str(self.workspace_port)
        return f"http://{self.agent_host}:{self.workspace_port}"