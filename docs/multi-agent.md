# Multi-Agent Projects

PulseBot supports **multi-agent projects** — coordinated groups of specialized AI agents that collaborate to complete complex tasks. Each project runs autonomously using a kanban-style message queue backed by Timeplus streams.

## Overview

A multi-agent project consists of:

- **ManagerAgent** — coordinates the project, dispatches tasks to workers, collects results, and delivers the final output to the user
- **SubAgents (workers)** — specialized agents that each handle a specific part of the work

Agents communicate asynchronously via the `pulsebot.kanban` stream. This decouples them from each other and from the main agent, enabling parallel or sequential workflows without blocking.

---

## Quick Start

Ask PulseBot to create a project using natural language:

> Create a multi-agent project with a Researcher and an Analyst. The Researcher should find 3 interesting facts about Python, and the Analyst should summarize them.

PulseBot calls the `create_project` tool internally with the appropriate configuration and spawns all agents as background asyncio tasks.

---

## How It Works

```
User
  │
  │  (asks for a multi-agent task)
  ▼
Main Agent
  │  calls create_project tool
  ▼
ProjectManager
  │  spawns ManagerAgent + worker SubAgents
  │
  ├──► ManagerAgent ──────────────────────────────────────────┐
  │      │                                                     │
  │      │  inserts task messages into pulsebot.kanban         │
  │      ▼                                                     │
  │    SubAgent A (Researcher)                                 │
  │      │  runs LLM loop                                      │
  │      │  writes result to pulsebot.kanban (target: Agent B) │
  │      ▼                                                     │
  │    SubAgent B (Analyst)                                    │
  │      │  runs LLM loop                                      │
  │      │  writes result to pulsebot.kanban (target: Manager) │
  │      ▼                                                     │
  └──── ManagerAgent receives result ◄──────────────────────┘
           │  writes final answer to pulsebot.messages
           ▼
         User (WebUI / Telegram)
```

### Message Routing

Messages in `pulsebot.kanban` are routed by `target_id` and `msg_type`:

| Sender → Target | `msg_type` | Why |
|-----------------|------------|-----|
| Manager → Worker | `task` | Workers listen for `task` and `control` messages |
| Worker → Worker | `task` | Same — receiving worker must see it as a task |
| Worker → Manager | `result` | Manager listens for `result`, `error`, `status` |
| Manager → Worker | `control` | Used to send `cancel` at project completion |

---

## Creating a Project

### Via Natural Language

Simply describe what you want to accomplish and how to divide the work. PulseBot will structure the agents appropriately.

### Via Direct Tool Call (API / SDK)

The `create_project` tool accepts:

```json
{
  "name": "Python Facts Project",
  "description": "Research and summarize Python facts",
  "session_id": "<current-session-id>",
  "agents": [
    {
      "name": "Researcher",
      "task_description": "Find 3 interesting facts about Python programming language.",
      "target_agents": ["Analyst"],
      "skills": ["shell"]
    },
    {
      "name": "Analyst",
      "task_description": "Summarize the research findings into a concise report.",
      "target_agents": []
    }
  ],
  "initial_messages": [
    {
      "target": "Researcher",
      "content": "Find 3 interesting facts about Python."
    }
  ]
}
```

**Agent spec fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Human-readable name. Auto-converted to `agent_<slug>` ID. |
| `task_description` | Yes | System-level role instructions for this agent. |
| `target_agents` | Yes | Agents to send results to. Empty list = send to manager. |
| `skills` | No | Skill subset to load. Omit to inherit all main agent skills. |
| `model` | No | Override LLM model (e.g., `"gpt-4o"`). |
| `provider` | No | Override LLM provider (e.g., `"openai"`). |

### Agent Naming and IDs

Agent names are automatically converted to IDs:

| Name | Agent ID |
|------|----------|
| `Researcher` | `agent_researcher` |
| `SQL Analyst` | `agent_sql_analyst` |
| `Report Writer` | `agent_report_writer` |

In `target_agents`, you can use human-readable names (`"Analyst"`) or agent IDs (`"agent_analyst"`) — both are resolved correctly.

---

## Workflow Patterns

### Sequential Pipeline

Agents form a chain where each agent's output feeds the next:

```
Manager → Agent A → Agent B → Agent C → Manager → User
```

Configure by setting `target_agents` to point to the next agent:

```json
"agents": [
  {"name": "Researcher", "target_agents": ["Analyst"], ...},
  {"name": "Analyst",    "target_agents": ["Writer"],  ...},
  {"name": "Writer",     "target_agents": [],           ...}
]
```

### Fan-Out (Parallel then Collect)

Manager dispatches independent tasks to multiple agents, collects their results:

```
Manager ─┬─► Agent A ─┐
          ├─► Agent B ─┤─► Manager → User
          └─► Agent C ─┘
```

All agents send their results back to the manager (empty `target_agents`). The manager delivers the first result it receives as the final output.

### Single-Agent Delegation

For simpler tasks, delegate to one specialized worker:

```
Manager → Worker → Manager → User
```

---

## Skills Per Agent

By default each worker inherits all skills loaded in the main agent. You can restrict a worker to a subset:

```json
{
  "name": "Shell Worker",
  "task_description": "Run system commands",
  "target_agents": [],
  "skills": ["shell"]
}
```

Valid skill names match the `builtin` list in `config.yaml`:
- `file_ops` — file read/write
- `shell` — shell command execution
- `workspace` — create web apps and file artifacts
- `scheduler` — manage recurring tasks

To give a worker **no tools** (pure reasoning only), pass an empty list: `"skills": []`.

---

## Model Overrides Per Agent

Each worker can use a different LLM model or provider:

```json
{
  "name": "Code Reviewer",
  "task_description": "Review Python code for bugs.",
  "target_agents": [],
  "provider": "anthropic",
  "model": "claude-opus-4-6"
}
```

Workers that don't specify `model`/`provider` inherit the main agent's LLM configuration.

---

## Kanban Streams

The multi-agent system uses three dedicated Timeplus streams:

### `pulsebot.kanban`

Inter-agent message queue.

| Column | Type | Description |
|--------|------|-------------|
| `msg_id` | string | Unique message ID (UUID) |
| `timestamp` | datetime64(3) | Message timestamp |
| `project_id` | string | Project this message belongs to |
| `sender_id` | string | Agent that sent the message |
| `target_id` | string | Agent that should receive it |
| `msg_type` | string | `task`, `result`, `error`, `status`, `control` |
| `content` | string | Message content / task description |
| `metadata` | string | JSON: source_msg_id, etc. |

### `pulsebot.kanban_projects`

Project lifecycle metadata.

| Column | Type | Description |
|--------|------|-------------|
| `project_id` | string | Unique project identifier |
| `name` | string | Human-readable project name |
| `description` | string | Project goal |
| `status` | string | `active`, `completed`, `failed`, `cancelled` |
| `created_by` | string | Originating agent or user |
| `session_id` | string | User session for routing final result |
| `agent_ids` | array(string) | All worker agent IDs |

### `pulsebot.kanban_agents`

Per-agent state and checkpoints.

| Column | Type | Description |
|--------|------|-------------|
| `agent_id` | string | Agent identifier |
| `project_id` | string | Project this agent belongs to |
| `name` | string | Agent name |
| `role` | string | `manager` or `worker` |
| `task_description` | string | Agent's system prompt |
| `target_agents` | array(string) | Downstream agent IDs |
| `status` | string | `pending`, `running`, `completed`, `failed` |
| `skills` | array(string) | Loaded skill names |
| `config` | string | JSON: model, provider, temperature, etc. |
| `checkpoint_sn` | int64 | Last processed `_tp_sn` for resumability |

---

## Project Management Tools

The `project_manager` skill exposes four tools to the main agent:

| Tool | Description |
|------|-------------|
| `create_project` | Create a new project and spawn all agents |
| `list_projects` | List all active and recent projects |
| `get_project_status` | Get detailed status of a specific project |
| `cancel_project` | Cancel a running project and stop all agents |

The `project_manager` skill must be enabled in `config.yaml`:

```yaml
skills:
  builtin:
    - project_manager
    # ... other skills
```

---

## Configuration

The `multi_agent` section in `config.yaml` controls resource limits:

```yaml
multi_agent:
  enabled: true
  max_agents_per_project: 10      # Hard cap on sub-agents per project
  max_concurrent_projects: 5      # Max simultaneously active projects
  default_agent_timeout: 300      # Per-agent task timeout (seconds)
  project_timeout: 1800           # Whole-project wall-clock timeout (seconds)
  checkpoint_interval: 1          # Checkpoint every N processed messages
```

| Field | Default | Description |
|-------|---------|-------------|
| `enabled` | `true` | Enable multi-agent coordination |
| `max_agents_per_project` | `10` | Maximum worker agents per project |
| `max_concurrent_projects` | `5` | Maximum simultaneously active projects |
| `default_agent_timeout` | `300` | Per-agent timeout in seconds |
| `project_timeout` | `1800` | Total project timeout in seconds |
| `checkpoint_interval` | `1` | How often to save agent checkpoints |

---

## Observability

Query the kanban streams directly to inspect project state:

```sql
-- See all messages for a project
SELECT * FROM table(pulsebot.kanban)
WHERE project_id = 'proj_abc123'
ORDER BY timestamp;

-- Check project status
SELECT project_id, name, status, agent_ids
FROM table(pulsebot.kanban_projects)
WHERE project_id = 'proj_abc123';

-- Check agent checkpoints
SELECT agent_id, status, checkpoint_sn
FROM table(pulsebot.kanban_agents)
WHERE project_id = 'proj_abc123';
```

---

## Limitations

- **Single result collection**: The ManagerAgent delivers the first `result` message it receives and then cancels remaining workers. For fan-out patterns where you need to aggregate multiple results, the Analyst agent should aggregate them before sending a single result to the manager.
- **No cross-project communication**: Agents in different projects cannot communicate directly.
- **LLM awareness**: Workers only know about their task description and available tools. They don't inherently know about other agents in the project unless you mention them in the task description.
- **Idle connection timeout**: Long-running projects may hit Timeplus streaming connection idle timeouts (~3 minutes). Ensure agent tasks complete within this window or configure appropriate keep-alive settings.
