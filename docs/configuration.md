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
| `provider` | `anthropic` | LLM provider to use. Supported: `anthropic`, `openai`, `openrouter`, `ollama`, `nvidia`, `gemini`. Set to `openai` with a `providers.openai.base_url` for any OpenAI-compatible vendor (Qwen, DeepSeek, etc.). |
| `temperature` | `0.7` | Controls randomness (0.0=deterministic, 1.0=creative). |
| `max_tokens` | `4096` | Maximum length of agent responses. |
| `max_iterations` | `15` | Maximum number of reasoning iterations per task. |
| `verbose_tools` | `false` | Enable detailed logging of tool execution. |

### Timeplus
Connection settings for the Timeplus / Proton database.

| Field | Default | Description |
| :--- | :--- | :--- |
| `host` | `${TIMEPLUS_HOST:-localhost}` | Database server hostname. |
| `port` | `8463` | Database server port. |
| `username` | `${TIMEPLUS_USER:-default}` | Authentication username. |
| `password` | `""` | Authentication password. |

### Providers
Configurations for specific LLM providers. Set `agent.provider` to the key name of the provider you want to use.

#### Anthropic
| Field | Default | Description |
| :--- | :--- | :--- |
| `api_key` | `""` | Anthropic API key. |
| `default_model` | `claude-sonnet-4-20250514` | Default model name. |

#### OpenAI (and OpenAI-compatible vendors)

The `openai` provider supports **any vendor that exposes an OpenAI-compatible API** — not just OpenAI itself. Set `agent.provider: openai` and configure a `base_url` to point at a different endpoint.

| Field | Default | Description |
| :--- | :--- | :--- |
| `api_key` | `""` | API key for the service. |
| `default_model` | `gpt-4o` | Default model name. |
| `base_url` | _(unset, uses OpenAI)_ | Custom API base URL for OpenAI-compatible vendors. |
| `provider_name` | _(auto-derived)_ | Optional display name shown in logs (auto-derived from `base_url` host when omitted). |

**Example — Alibaba Qwen (DashScope):**
```yaml
agent:
  provider: openai
  model: qwen-max

providers:
  openai:
    api_key: "${DASHSCOPE_API_KEY}"
    default_model: qwen-max
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    provider_name: "alibaba_qwen"   # optional, for log clarity
```

**Example — DeepSeek:**
```yaml
providers:
  openai:
    api_key: "${DEEPSEEK_API_KEY}"
    default_model: deepseek-chat
    base_url: "https://api.deepseek.com/v1"
```

#### OpenRouter
A pre-configured shortcut that routes to [openrouter.ai](https://openrouter.ai). Use `agent.provider: openrouter`.

| Field | Default | Description |
| :--- | :--- | :--- |
| `api_key` | `""` | OpenRouter API key. |
| `default_model` | `anthropic/claude-sonnet-4-20250514` | Default model (uses OpenRouter model IDs). |
| `base_url` | `https://openrouter.ai/api/v1` | Base URL (override only if needed). |

#### NVIDIA
| Field | Default | Description |
| :--- | :--- | :--- |
| `api_key` | `""` | NVIDIA API key. |
| `default_model` | `moonshotai/kimi-k2.5` | Default model name. |
| `timeout_seconds` | `120` | Request timeout. |
| `enable_thinking` | `false` | Enable deep thinking mode. |

#### Gemini
| Field | Default | Description |
| :--- | :--- | :--- |
| `api_key` | `""` | Google Gemini API key. |
| `default_model` | `gemini-2.5-flash` | Default model name. |
| `timeout_seconds` | `120` | Request timeout. |

#### Ollama (Local LLM)
| Field | Default | Description |
| :--- | :--- | :--- |
| `enabled` | `false` | Enable local LLM support. |
| `host` | `http://localhost:11434` | Ollama server address. |
| `default_model` | `llama3` | Local model name. |
| `timeout_seconds` | `120` | Request timeout. |

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
| `builtin` | List of standard skills (e.g., `file_ops`, `shell`, `workspace`, `scheduler`). |
| `custom` | List of additional skill names to load. |
| `skill_dirs` | Directories to scan for custom skill packages. |
| `disabled_skills` | Specific skills to skip during loading. |

Available built-in skills:

| Skill | Description |
| :--- | :--- |
| `file_ops` | Sandboxed file read/write/list operations. |
| `shell` | Shell execution with security guards. |
| `workspace` | Create and publish dynamic artifacts and web apps. |
| `scheduler` | Create and manage recurring tasks backed by Timeplus native Tasks. |

#### Scheduler Skill

The `scheduler` skill is automatically wired at startup and requires the `workspace.api_server_url` field to be reachable from inside the agent. Each Timeplus TASK embeds a Python UDF that POSTs to `{api_server_url}/api/v1/task-trigger` when it fires.

> **Docker deployments**: set `workspace.api_server_url` to the internal Docker service URL (e.g., `http://pulsebot-api:8000`) so the UDF can reach the API server from inside the Timeplus container.

Example config snipped:

```yaml
skills:
  builtin:
    - file_ops
    - shell
    - workspace
    - scheduler

workspace:
  api_server_url: "http://localhost:8000"   # or http://pulsebot-api:8000 in Docker
```

### Memory
Vector-based memory for context retention and duplicate detection.

| Field | Default | Description |
| :--- | :--- | :--- |
| `enabled` | `true` | Enable the memory system. |
| `similarity_threshold`| `0.95` | Sensitivity for finding similar items (0.0 to 1.0). |
| `embedding_provider` | `openai` | Provider for vector embeddings (`openai` or `ollama`). |
| `embedding_model` | `text-embedding-3-small` | Model used for generating embeddings. |
| `embedding_api_key` | `""` | Override API key for OpenAI embeddings (optional). |
| `embedding_host` | `""` | Override host for Ollama embeddings (optional). |
| `embedding_dimensions` | `""` | Dimension of the embeddings (auto-detected if unset). |
| `embedding_timeout_seconds` | `30` | Timeout limit for embedding requests. |

### Workspace
Orchestration settings for the agent-side workspaces.

| Field | Default | Description |
| :--- | :--- | :--- |
| `base_dir` | `./workspaces` | Directory where workspace artifacts are stored. |
| `workspace_port` | `8001` | Port for the agent's internal workspace server. |
| `agent_host` | `localhost` | Hostname the API server uses to reach the agent. |
| `api_server_url` | `http://localhost:8000` | API server base URL for agent to register artifacts and for the scheduler UDF to call back into. |
| `backend_boot_timeout`| `3.0` | Seconds to wait after spawning a backend subprocess before health-checking. |
| `internal_api_key` | `""` | Shared secret for agent-to-API-server registration. |

### Hooks

Intercept tool calls before and after execution. Hooks are organized by call type under the top-level `hooks:` key, making it easy to add new hook types (e.g., `llm_call`) in the future.

#### `hooks.tool_call`

Controls the pre/post hook chain for every tool call the agent makes.

| Field | Default | Description |
| :--- | :--- | :--- |
| `pre_call` | `[]` | Ordered list of hook entries to run before tool execution. If empty, a `PassthroughHook` (zero-overhead) is used. |

Each entry in `pre_call` has:

| Field | Description |
| :--- | :--- |
| `type` | Hook type: `passthrough`, `policy`, or `webhook`. |
| `config` | Hook-specific configuration (see below). |

**Built-in hook types:**

| Type | Description |
| :--- | :--- |
| `passthrough` | Approves every call unconditionally. Default when no hooks are configured. |
| `policy` | Allow/deny by tool name (supports `*` wildcards) and argument regex patterns. |
| `webhook` | POSTs call info to an external HTTP endpoint; uses the response verdict. |

**`policy` config options:**

| Field | Description |
| :--- | :--- |
| `allow_tools` | Whitelist of tool name patterns (fnmatch). Only listed tools are approved. |
| `deny_tools` | Blacklist of tool name patterns. Takes precedence over `allow_tools`. |
| `deny_argument_patterns` | Map of argument key → list of regex patterns to block. |

**`webhook` config options:**

| Field | Default | Description |
| :--- | :--- | :--- |
| `url` | _(required)_ | HTTP/HTTPS endpoint to POST to. |
| `auth_header` | `""` | Optional `Authorization` header value. |
| `timeout` | `5.0` | Request timeout in seconds. |
| `fail_open` | `true` | If `true`, approve on network errors. If `false`, deny on errors. |

**Example:**

```yaml
hooks:
  tool_call:
    pre_call:
      # Block shell access, allow only file tools
      - type: policy
        config:
          deny_tools: ["run_command"]
          allow_tools: ["read_file", "write_file", "list_directory"]

      # Also check with an external approval service
      - type: webhook
        config:
          url: "https://your-approval-service.example.com/hook"
          auth_header: "Bearer ${WEBHOOK_SECRET}"
          timeout: 5.0
          fail_open: true
```

See [Tool Call Hooks](hooks.md) for full details.

### Multi-Agent

Controls resource limits for multi-agent projects. Requires the `project_manager` skill to be enabled.

| Field | Default | Description |
| :--- | :--- | :--- |
| `enabled` | `true` | Enable multi-agent coordination. |
| `max_agents_per_project` | `10` | Maximum number of worker agents per project. |
| `max_concurrent_projects` | `5` | Maximum number of simultaneously active projects. |
| `default_agent_timeout` | `300` | Per-agent task timeout in seconds. |
| `project_timeout` | `1800` | Whole-project wall-clock timeout in seconds. |
| `checkpoint_interval` | `1` | Checkpoint every N processed kanban messages. |

Example:

```yaml
multi_agent:
  enabled: true
  max_agents_per_project: 10
  max_concurrent_projects: 5
  default_agent_timeout: 300
  project_timeout: 1800
  checkpoint_interval: 1
```

To enable multi-agent support, also add `project_manager` to your builtin skills:

```yaml
skills:
  builtin:
    - file_ops
    - shell
    - project_manager
```

See [Multi-Agent Projects](multi-agent.md) for full documentation.

### Other Sections
- **API**: Controls the main API server (`host`, `port`, `cors_origins`).
- **Logging**: Set `level` (DEBUG, INFO, etc.) and `format` (`json` or `text`).
- **Scheduled Tasks**: Configure background jobs like `heartbeat` or `daily_summary`.
- **MCP Servers**: Configure external Model Context Protocol servers.
