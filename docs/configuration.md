# Configuration Guide

PulseBot uses a flexible configuration system based on YAML files and environment variables. This document describes all available settings and how they are loaded.

## Loading Logic

PulseBot primarily reads from `config.yaml`. Values can be overridden or defined using environment variables. The system also supports dynamic variable substitution within the YAML file.

### Environment Variable Substitution
You can use `${VAR_NAME}` or `${VAR_NAME:-default}` syntax in your `config.yaml`.
- `${TIMEPLUS_HOST}`: Replaced by the value of `TIMEPLUS_HOST`.
- `${TIMEPLUS_HOST:-localhost}`: Replaced by `TIMEPLUS_HOST`, or `localhost` if the variable is unset.

---

## Configuration Sections

### Agent
General identity and behavioral settings for the AI agent.

| Field | Default | Description |
| :--- | :--- | :--- |
| `name` | `PulseBot` | The name the agent uses to identify itself. |
| `model` | `claude-sonnet-4-20250514` | The default LLM model to use. |
| `provider` | `anthropic` | The primary LLM provider (e.g., `openai`, `ollama`). |
| `temperature` | `0.7` | Controls randomness (0.0=deterministic, 1.0=creative). |
| `max_tokens` | `4096` | Maximum length of agent responses. |

### Timeplus
Connection settings for the Timeplus / Proton database.

| Field | Default | Description |
| :--- | :--- | :--- |
| `host` | `${TIMEPLUS_HOST:-localhost}` | Database server hostname. |
| `port` | `8463` | Database server port. |
| `username` | `${TIMEPLUS_USER:-default}` | Authentication username. |
| `password` | `""` | Authentication password. |

### Providers
Configurations for specific LLM providers.

- **Anthropic / OpenAI / OpenRouter / NVIDIA**:
  - `api_key`: Secret API key for the service.
  - `default_model`: Override model for this specific provider.
- **Ollama (Local LLM)**:
  - `enabled`: Set to `true` to enable local LLM support.
  - `host`: Address of the Ollama server (default `http://localhost:11434`).
  - `default_model`: Local model name (e.g., `llama3`).

### Channels
Settings for different user interaction interfaces.

- **Telegram**:
  - `enabled`: Enable/disable Telegram bot.
  - `token`: Telegram Bot API token.
  - `allow_from`: List of Telegram user IDs permitted to use the bot.
- **Webchat**:
  - `enabled`: Enable the web UI (default `true`).
  - `port`: Port for the web interface (default `8000`).

### Skills
Control which tools the agent can access.

| Field | Description |
| :--- | :--- |
| `builtin` | List of standard skills (e.g., `web_search`, `file_ops`, `shell`, `workspace`). |
| `custom` | List of additional skill names to load. |
| `skill_dirs` | Directories to scan for custom skill packages. |
| `disabled_skills` | Specific skills to skip during loading. |

### Search
Web search provider settings.

| Field | Default | Description |
| :--- | :--- | :--- |
| `provider` | `brave` | Search engine to use (`brave` or `searxng`). |
| `brave_api_key` | `""` | API key for Brave Search. |
| `searxng_url` | `http://localhost:8080` | URL for the SearXNG instance. |

### Memory
Vector-based memory for context retention and duplicate detection.

| Field | Default | Description |
| :--- | :--- | :--- |
| `enabled` | `true` | Enable the memory system. |
| `similarity_threshold`| `0.95` | Sensitivity for finding similar items (0.0 to 1.0). |
| `embedding_provider` | `openai` | Provider for vector embeddings (`openai` or `ollama`). |
| `embedding_model` | `text-embedding-3-small` | Model used for generating embeddings. |

### Workspace
Orchestration settings for the agent-side workspaces.

| Field | Default | Description |
| :--- | :--- | :--- |
| `base_dir` | `./workspaces` | Directory where workspace artifacts are stored. |
| `workspace_port` | `8001` | Port for the agent's internal workspace server. |
| `internal_api_key` | `""` | Shared secret for agent-to-API-server registration. |
| `agent_host` | `localhost` | Hostname the API server uses to reach the agent. |

### Other Sections
- **API**: Controls the main API server (`host`, `port`, `cors_origins`).
- **Logging**: Set `level` (DEBUG, INFO, etc.) and `format` (`json` or `text`).
- **Scheduled Tasks**: Configure background jobs like `heartbeat` or `daily_summary`.
- **MCP Servers**: Configure external Model Context Protocol servers.
