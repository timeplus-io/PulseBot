# PulseBot: Technical Design Document

## A Lightweight, Stream-Native AI Agent Powered by Timeplus

**Version:** 2.0
**Author:** Timeplus Engineering

---

## 1. Executive Summary

PulseBot is an ultra-lightweight personal AI agent that leverages Timeplus's streaming SQL engine as its backbone for agent communication, memory management, and observability. It delivers equivalent functionality to complex agent frameworks in ~5,000 lines of Python by treating **everything as a stream**.

### Core Design Principles

1. **Stream-Native Architecture**: All agent communication, events, and state changes flow through Timeplus streams
2. **SQL-First Configuration**: Agents and workflows are defined and queried via streaming SQL
3. **Radical Simplicity**: Target ~5,000 lines of Python
4. **Observable by Default**: Every LLM call, tool execution, and agent decision is logged to streams
5. **Extensible Plugin System**: Channels and skills as pluggable modules

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Clients                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │  Web Chat   │    │     CLI     │    │  Telegram   │                      │
│  │  (Browser)  │    │  (Terminal) │    │    (Bot)    │                      │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                      │
│         │                  │                  │                              │
│         └──────────────────┼──────────────────┘                              │
│                            │                                                 │
│                   HTTP / WebSocket                                           │
│                            │                                                 │
│                            ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      API Server (FastAPI)                            │    │
│  │  • REST endpoints (/chat, /health, /sessions)                        │    │
│  │  • WebSocket real-time chat (/ws/{session_id})                       │    │
│  │  • Serves web UI (static HTML/CSS/JS)                                │    │
│  └───────────────────────────┬─────────────────────────────────────────┘    │
│                              │                                               │
│              ┌───────────────┴───────────────┐                               │
│              │                               │                               │
│           writes                          reads                              │
│       (user_input)              (agent_response, tool_call)                  │
│              │                               │                               │
│              ▼                               ▼                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    Timeplus Proton (Streaming Database)                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Streams                                        │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌────────┐  ┌────────┐  ┌──────────────┐  │  │
│  │  │ messages  │  │ llm_logs  │  │ tool_logs │  │ memory │  │ events │  │task_triggers │  │  │
│  │  │           │  │           │  │           │  │        │  │        │  │              │  │  │
│  │  │ user_input│  │ tokens    │  │ tool_name │  │ content│  │ type   │  │ trigger_id   │  │  │
│  │  │ agent_resp│  │ latency   │  │ duration  │  │ embed  │  │ payload│  │ task_name    │  │  │
│  │  │ tool_call │  │ cost      │  │ status    │  │ score  │  │ tags   │  │ prompt       │  │  │
│  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └───┬────┘  └───┬────┘  └──────┬───────┘  │  │
│  │        │              │              │            │           │               │           │  │
│  │   API Server       Agent          Agent        Agent       Agent+Tasks    Timeplus       │  │
│  │   writes/reads     writes         writes       writes      writes         Tasks write    │  │
│  └───────────────────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                 listens                       writes
              (user_input)       (agent_response, tool_call, llm_logs,
                    │                  tool_logs, memory)
                    ▼                             │
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Agent Core                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Agent Loop                                     │  │
│  │                                                                        │  │
│  │  1. Listen for user_input messages                                     │  │
│  │  2. Build context (history + memories)                                 │  │
│  │  3. Call LLM provider                                                  │  │
│  │  4. Execute tools if requested                                         │  │
│  │  5. Write responses back to messages stream                            │  │
│  │  6. Log to llm_logs and tool_logs                                      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                              │                                               │
│              ┌───────────────┼───────────────┐                               │
│              │               │               │                               │
│              ▼               ▼               ▼                               │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                    │
│  │ Context       │  │ LLM Providers │  │ Tool Executor │                    │
│  │ Builder       │  │               │  │               │                    │
│  │               │  │ • Anthropic   │  │ • Skills      │                    │
│  │ • History     │  │ • OpenAI      │  │   - shell     │                    │
│  │ • Memory      │  │ • Ollama      │  │   - file_ops  │                    │
│  │ • System      │  │ • OpenRouter  │  │               │                    │
│  │   prompt      │  │ • NVIDIA      │  │               │                    │
│  └───────────────┘  └───────────────┘  └───────────────┘                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Client → API Server**: User sends message via HTTP/WebSocket
2. **API Server → messages stream**: Writes `user_input` message
3. **Agent ← messages stream**: Listens for new `user_input` messages
4. **Agent → LLM Provider**: Builds context and calls LLM
5. **Agent → llm_logs stream**: Logs tokens, latency, cost
6. **Agent → Tools**: Executes tools if LLM requests them
7. **Agent → tool_logs stream**: Logs tool execution details
8. **Agent → memory stream**: Stores extracted memories (optional)
9. **Agent → messages stream**: Writes `agent_response` and `tool_call` messages
10. **API Server ← messages stream**: Listens for responses on the session
11. **Client ← API Server**: Forwards responses via WebSocket

**Scheduled Task Data Flow:**

12. **Timeplus Task → Python UDF**: Task fires on its schedule
13. **Python UDF → `/api/v1/task-trigger`**: HTTP POST to PulseBot API
14. **API Server → messages stream**: Writes `scheduled_task` message with global session
15. **Agent ← messages stream**: Picks up `scheduled_task`, processes with LLM
16. **Agent → NotificationDispatcher**: Sends result text to dispatcher
17. **NotificationDispatcher → events stream**: Writes `task_notification` event
18. **Telegram / WebSocket ← events stream**: All channel adapters fan out to their active connections

### Stream Ownership

| Stream | Writer | Reader |
|--------|--------|--------|
| messages | API Server (user_input), Agent (agent_response, tool_call) | Agent, API Server |
| llm_logs | Agent | Analytics/Dashboards |
| tool_logs | Agent | Analytics/Dashboards |
| memory | Agent | Agent (context builder) |
| events | Agent (NotificationDispatcher) | Telegram, WebSocket (task_notification), Monitoring |
| task_triggers | Timeplus Tasks (via Python UDF) | Audit/Analytics |

---

## 3. Core Timeplus Streams

All data flows through five core streams. Streams are created automatically on agent startup using `CREATE STREAM IF NOT EXISTS`.

### 3.1 Messages Stream

Central communication hub for all agent interactions.

| Column | Type | Description |
|--------|------|-------------|
| id | string | Unique message ID (UUID) |
| timestamp | datetime64(3) | Event timestamp |
| source | string | Origin: 'telegram', 'webchat', 'agent', 'skill', 'system' |
| target | string | Destination: 'agent', 'channel:telegram', 'broadcast' |
| session_id | string | Groups related messages |
| message_type | string | 'user_input', 'agent_response', 'tool_call', 'tool_result', 'error' |
| content | string | JSON payload |
| user_id | string | User identifier |
| channel_metadata | string | Channel-specific data (JSON) |
| priority | int8 | Priority level (-1 to 2) |

### 3.2 LLM Logs Stream

Comprehensive observability for all LLM calls.

| Column | Type | Description |
|--------|------|-------------|
| id | string | Request ID |
| timestamp | datetime64(3) | Call timestamp |
| session_id | string | Associated session |
| model | string | Model name (e.g., 'claude-sonnet-4-20250514') |
| provider | string | Provider name ('anthropic', 'openai', 'ollama') |
| input_tokens | int32 | Input token count |
| output_tokens | int32 | Output token count |
| total_tokens | int32 | Total token count |
| estimated_cost_usd | float32 | Estimated cost |
| latency_ms | int32 | Total latency |
| time_to_first_token_ms | int32 | Streaming latency |
| system_prompt_hash | string | SHA256 of system prompt |
| user_message_preview | string | First 200 chars of user message |
| assistant_response_preview | string | First 200 chars of response |
| tools_called | array(string) | List of tool names called |
| tool_call_count | int8 | Number of tool calls |
| status | string | 'success', 'error', 'rate_limited', 'timeout' |
| error_message | string | Error details if failed |

### 3.3 Tool Logs Stream

Dedicated logging for tool executions with timing and status.

| Column | Type | Description |
|--------|------|-------------|
| id | string | Log entry ID |
| timestamp | datetime64(3) | Execution timestamp |
| session_id | string | Associated session |
| llm_request_id | string | Links to triggering LLM call |
| tool_name | string | Name of tool executed |
| skill_name | string | Parent skill name |
| arguments | string | JSON of tool arguments |
| status | string | 'started', 'success', 'error' |
| result_preview | string | First 500 chars of result |
| error_message | string | Error details if failed |
| duration_ms | int32 | Execution duration |

### 3.4 Memory Stream

Persistent memory with vector search capability using append-only design with soft delete.

| Column | Type | Description |
|--------|------|-------------|
| id | string | Memory ID |
| timestamp | datetime64(3) | Creation timestamp |
| memory_type | string | 'fact', 'preference', 'conversation_summary', 'skill_learned' |
| category | string | 'user_info', 'project', 'schedule', 'general' |
| content | string | The memory content |
| source_session_id | string | Originating session |
| embedding | array(float32) | Vector embedding (1536-dim for OpenAI) |
| importance | float32 | 0.0 to 1.0, affects retrieval priority |
| is_deleted | bool | Soft delete flag (append-only pattern) |

**Memory Features:**
- Semantic search using cosine similarity
- Hybrid scoring: vector similarity weighted by importance
- Optional feature - requires OpenAI API key for embeddings
- Soft delete pattern for append-only streams

### 3.5 Events Stream

System events for monitoring, alerting, and cross-channel broadcast.

| Column | Type | Description |
|--------|------|-------------|
| id | string | Event ID |
| timestamp | datetime64(3) | Event timestamp |
| event_type | string | `'heartbeat'`, `'channel_connected'`, `'skill_loaded'`, `'error'`, `'alert'`, **`'task_notification'`** |
| source | string | Event source |
| severity | string | `'debug'`, `'info'`, `'warning'`, `'error'`, `'critical'` |
| payload | string | JSON event data |
| tags | array(string) | Filtering tags |

The `task_notification` event type is written by `NotificationDispatcher` after every scheduled task execution. Its `payload` JSON contains `task_name`, `text`, and `session_id`.

### 3.6 Task Triggers Stream

Audit log for every scheduled task invocation — inserted by the Timeplus Python UDFs embedded in each TASK.

| Column | Type | Description |
|--------|------|-------------|
| trigger_id | string | UUID for this invocation |
| task_id | string | Sanitised internal task name |
| task_name | string | Same as task_id |
| prompt | string | Instruction executed on this run |
| execution_id | string | UUID returned by `/api/v1/task-trigger` |
| triggered_at | datetime64(3) | UTC timestamp of invocation |

---

## 4. Agent Core Components

### 4.1 Agent Loop

The main processing loop that:
1. Listens to the messages stream for incoming requests (`user_input` and `scheduled_task`)
2. Builds context from memory and conversation history
3. Calls LLM for reasoning
4. Executes tools and writes results back to stream
5. Broadcasts tool call status to UI/CLI in real-time
6. Routes `scheduled_task` messages through `NotificationDispatcher` instead of a normal channel response

**Features:**
- Maximum 10 iterations per request (prevent infinite loops)
- Automatic stream creation on startup
- Tool call broadcasting for real-time UI updates
- Error handling with client notification

### 4.2 Context Builder

Assembles complete context for LLM prompts:
- System prompt with agent identity and instructions
- Conversation history from messages stream
- Relevant memories via vector search (if configured)
- Available tools from loaded skills

### 4.3 Tool Executor

Executes tools from loaded skills:
- Routes tool calls to appropriate skill
- Handles errors gracefully
- Returns structured results
- Logs execution to tool_logs stream

### 4.4 Router

Routes messages between components:
- Channel → Agent (user input)
- Agent → Channel (responses)
- Agent → Tools (execution)
- Tools → Agent (results)

### 4.5 NotificationDispatcher

Broadcasts scheduled-task results to all channels via the events stream.

- Receives the agent's response text after a `scheduled_task` execution
- Writes a `task_notification` event to `pulsebot.events`
- Channel adapters (Telegram, WebSocket) each subscribe independently and fan out to all active connections
- Decoupled: adding a new channel only requires subscribing to the events stream

---

## 5. LLM Providers

Multi-provider support with unified interface:

| Provider | Models | Features |
|----------|--------|----------|
| Anthropic | Claude 4 Opus, Claude 4.5 Sonnet | Primary provider, tool use |
| OpenAI | GPT-4o, GPT-4 Turbo | Alternative provider |
| Ollama | Llama 3, Mistral, etc. | Local development |
| OpenRouter | Multiple providers | Unified access to many models |
| NVIDIA | NIM models | Enterprise deployment |

---

## 6. Channels

Input/output channels for user interaction:

### 6.1 Web Chat (Built-in)

- Single-file HTML/CSS/JS interface
- WebSocket for real-time communication
- Tool call status indicators with animations
- Session-based conversation history
- Minimal dependencies

### 6.2 CLI

- Rich terminal UI with progress indicators
- Real-time tool call display
- Interactive chat mode
- Session management

### 6.3 Telegram

- Bot API integration
- User allowlist for security
- Persistent sessions per user
- Subscribes to `events` stream for `task_notification` events and broadcasts to all active chat IDs
- Restores sessions from message history on restart so task broadcasts survive agent restarts
- Falls back to `allow_from` list when no interactive sessions exist

---

## 7. Skills System

Pluggable tool system with base interface:

### Built-in Skills

| Skill | Tools | Description |
|-------|-------|-------------|
| shell | `run_command` | Shell execution with security guards |
| file_ops | `read_file`, `write_file`, `list_directory` | Sandboxed file operations |
| workspace | `workspace_create_app`, ... | Dynamic artifact and web-app publishing |
| scheduler | `create_interval_task`, `create_cron_task`, `list_tasks`, `pause_task`, `resume_task`, `delete_task` | LLM-callable task management backed by Timeplus native Tasks |


### Skill Interface

Skills implement:
- `get_tools()` - Return tool definitions
- `execute(tool_name, arguments)` - Execute a tool
- `name` and `description` properties

---

## 8. Real-time Features

### 8.1 Tool Call Broadcasting

Tool executions are broadcast in real-time:
1. **Started**: Tool name and formatted arguments
2. **Completed**: Success status with duration
3. **Error**: Error message with details

Displayed in:
- Web Chat: Animated indicators with shimmer effect
- CLI: Compact status lines with timing

### 8.2 WebSocket Streaming

Real-time message delivery via WebSocket:
- Agent responses stream as they're generated
- Tool call status updates
- Error notifications
- Connection state management

---

## 9. API Endpoints

### REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web chat interface |
| GET | `/health` | Health check |
| POST | `/chat` | Send message (async) |
| POST | `/api/v1/task-trigger` | Scheduled task callback from Timeplus Python UDF |
| GET | `/sessions/{id}/history` | Get conversation history |

### WebSocket

| Endpoint | Description |
|----------|-------------|
| `/ws/{session_id}` | Real-time bidirectional chat |

WebSocket message types:
- `message` — User input / agent response
- `tool_call` — Tool execution status
- `task_notification` — Scheduled task broadcast result
- `error` — Error notifications

---

## 10. Configuration

YAML-based configuration with environment variable substitution:

```yaml
agent:
  name: "PulseBot"
  model: "claude-sonnet-4-20250514"
  provider: "anthropic"

providers:
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
  openai:
    api_key: ${OPENAI_API_KEY}
  ollama:
    enabled: true
    host: "http://localhost:11434"

timeplus:
  host: "localhost"
  port: 8123

channels:
  telegram:
    enabled: true
    token: ${TELEGRAM_BOT_TOKEN}
  webchat:
    enabled: true
    port: 8000

skills:
  builtin:
    - shell
    - file_ops
    - scheduler
```

---

## 11. Deployment

### Docker Compose

Services:
- **Timeplus Proton** - Streaming database (ports 8123, 3218, 8463)
- **PulseBot Agent** - Message processing
- **PulseBot API** - REST/WebSocket interface (port 8000)

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| ANTHROPIC_API_KEY | Yes* | Claude API key |
| OPENAI_API_KEY | No | OpenAI key (also for memory embeddings) |
| TIMEPLUS_HOST | Yes | Timeplus host |
| TIMEPLUS_PASSWORD | No | Timeplus password |
| TELEGRAM_BOT_TOKEN | No | Telegram bot token |

*One LLM provider key required

---

## 12. CLI Commands

| Command | Description |
|---------|-------------|
| `pulsebot run` | Start the agent loop |
| `pulsebot serve` | Start FastAPI server |
| `pulsebot chat` | Interactive CLI chat |
| `pulsebot init` | Generate config.yaml |
| `pulsebot task list` | List all scheduled tasks |
| `pulsebot task create` | Create an interval or cron task |
| `pulsebot task pause <name>` | Pause a task |
| `pulsebot task resume <name>` | Resume a paused task |
| `pulsebot task delete <name>` | Delete a task |

---

## 13. Design Decisions

### Why Append-Only Streams for Memory?

Mutable streams are an enterprise feature. The memory system uses append-only streams with a soft delete pattern:
- `is_deleted` flag marks deleted records
- Queries filter `WHERE is_deleted = false`
- Simple and works with open-source Proton

### Why Optional Memory?

Memory requires OpenAI API for embeddings. When not configured:
- Memory features are gracefully disabled
- Agent works without semantic memory
- No errors or degraded experience

### Why Single-File Web UI?

- Zero build step required
- Easy to customize
- Minimal dependencies
- Fast to load and modify

### Why Tool Call Broadcasting?

Users need visibility into what the agent is doing:
- Shows tool name and summarized arguments
- Real-time status updates
- Duration tracking
- Error visibility

---

## 14. Future Enhancements

Planned features:
- MCP (Model Context Protocol) server support
- Additional channels (Slack, WhatsApp)
- Analytics dashboard
- Cost tracking views

---

## 15. Conclusion

PulseBot delivers a powerful, observable, and extensible AI agent by leveraging Timeplus's streaming SQL engine. The stream-native architecture provides:

1. **Simplicity**: ~5K lines of Python
2. **Observability**: Every event flows through queryable streams
3. **Extensibility**: Plugin-based skills and channels
4. **Real-time**: Sub-second message routing and tool status
5. **SQL-First**: Query and analyze everything via SQL
