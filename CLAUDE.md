# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PulseBot is a stream-native AI agent framework powered by Timeplus (streaming SQL database). All communication, events, and state changes flow through Timeplus streams rather than traditional file systems or databases.

## Common Commands

```bash
# CLI commands (after installation)
pulsebot run              # Start agent main loop (listens to message streams)
pulsebot serve            # Start FastAPI server on port 8000
pulsebot chat             # Interactive CLI chat
pulsebot setup            # Initialize Timeplus streams & database tables
pulsebot init             # Generate default config.yaml
pulsebot task list        # List scheduled tasks

# Development
pytest                    # Run all tests
pytest -v                 # Verbose test output
pytest --cov              # Run tests with coverage
ruff check .              # Lint code
mypy pulsebot/            # Type checking

# Docker deployment
docker-compose up -d      # Start all services (proton, postgres, agent, api)
```

## Architecture

### Stream-Native Communication

All components communicate via Timeplus streams (unbounded append-only data):

1. **Input Channels** (Telegram, Webchat) → Write to `messages` stream
2. **Agent Core** → Reads from `messages`, processes via LLM, writes responses back
3. **Skills/Tools** → Execute when called, results flow back through messages
4. **Observability** → All LLM calls logged to `llm_logs` stream, memories to `memory` stream

### Agent Loop (core/agent.py)

```
1. Listen for messages targeting 'agent' on messages stream
2. For each message:
   a. Build context (conversation history + relevant memories via vector search)
   b. Get available tools from loaded skills
   c. Loop (max 10 iterations):
      - Call LLM with context + tools
      - Log call to llm_logs stream
      - If tool calls: execute tools, add results to context
      - Else: send response, extract/store memories, break
```

### Key Source Directories

- `pulsebot/core/` - Agent loop, context building, tool execution, routing
- `pulsebot/providers/` - LLM provider implementations (Anthropic, OpenAI, OpenRouter, Ollama)
- `pulsebot/skills/` - Tool/skill system with builtin skills (web_search, file_ops, shell)
- `pulsebot/channels/` - Input channels (Telegram bot integration)
- `pulsebot/timeplus/` - Timeplus client, stream reader/writer, vector memory, scheduled tasks
- `pulsebot/db/` - PostgreSQL metadata storage (SQLAlchemy models)
- `pulsebot/api/` - FastAPI server with REST and WebSocket endpoints

### Timeplus Streams

| Stream | Purpose |
|--------|---------|
| `messages` | Central communication hub (source, target, session_id, content) |
| `llm_logs` | LLM call observability (model, tokens, latency, status) |
| `memory` | Vector-indexed knowledge base with embeddings |
| `events` | System events and alerts |

### Design Patterns

**Provider Pattern**: All LLM providers implement `LLMProvider` base class with `async chat()` returning `LLMResponse`

**Skill Pattern**: Skills inherit from `BaseSkill` with `get_tools()` → `ToolDefinition` and `async execute()` → `ToolResult`

**Stream Operations**: `StreamReader` for async iteration, `StreamWriter` for writes, `TimeplusClient` for low-level protocol

## Configuration

`config.yaml` uses Pydantic validation with environment variable substitution (`${VAR_NAME}` or `${VAR_NAME:-default}`):
- `agent`: name, model, provider, temperature
- `timeplus`: host, port, credentials
- `postgres`: connection details
- `providers`: API keys for Anthropic, OpenAI, OpenRouter, Ollama
- `channels`: Telegram settings
- `skills`: enabled builtin skills

## Requirements

- Python 3.11+
- Timeplus/Proton (streaming database, port 8463)
- PostgreSQL (metadata storage)
