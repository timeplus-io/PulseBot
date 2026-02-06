# PulseBot: Technical Design Document

## A Lightweight, Stream-Native AI Agent Powered by Timeplus

**Version:** 1.0  
**Author:** Timeplus Engineering  
**Target:** \~5,000 lines of Python code

---

## 1\. Executive Summary

PulseBot is an ultra-lightweight personal AI agent that leverages Timeplus's streaming SQL engine as its backbone for agent communication, task scheduling, data ingestion, memory management, and observability. Unlike OpenClaw's 430K+ lines of TypeScript with file-based memory and cron-based heartbeats, PulseBot delivers equivalent functionality in \~5,000 lines of Python by treating **everything as a stream**.

### Core Design Principles

1. **Stream-Native Architecture**: All agent communication, events, and state changes flow through Timeplus streams  
2. **SQL-First Configuration**: Agents, skills, and workflows are defined and queried via streaming SQL  
3. **Radical Simplicity**: Target \~5,000 lines of Python (inspired by nanobot's \~4,000 lines)  
4. **Observable by Default**: Every LLM call, tool execution, and agent decision is logged to streams  
5. **Extensible Plugin System**: Channels, skills, and MCP servers as pluggable modules

---

## 2\. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PulseBot                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   Channels   │    │    Skills    │    │ MCP Servers  │                   │
│  │  (Telegram,  │    │  (Weather,   │    │  (External   │                   │
│  │   WhatsApp,  │    │   GitHub,    │    │   Tools)     │                   │
│  │   Slack...)  │    │   Custom...) │    │              │                   │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                   │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Message Bus (Timeplus Streams)                   │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │   │
│  │  │  messages   │ │   events    │ │  llm_logs   │ │   memory    │   │   │
│  │  │   stream    │ │   stream    │ │   stream    │ │   stream    │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         Agent Core                                   │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │   │
│  │  │   Router    │ │  Agent Loop │ │   Context   │ │    Tool     │   │   │
│  │  │             │ │             │ │   Builder   │ │  Executor   │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Timeplus Proton Engine                            │   │
│  │  • Streaming SQL    • Materialized Views    • Tasks (Scheduling)    │   │
│  │  • Vector Search    • External Streams      • Real-time Analytics   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────┐                                                        │
│  │   PostgreSQL    │  (Metadata: configs, agents, skills registry)         │
│  └─────────────────┘                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           Frontend (React + JS)                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  Dashboard  │ │   Chat UI   │ │  Analytics  │ │   Config    │           │
│  │  (Streams)  │ │             │ │  (Charts)   │ │   Editor    │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3\. Core Timeplus Streams Schema

### 3.1 Message Stream (Agent Communication Hub)

All inter-component communication flows through this single stream:

```sql
CREATE STREAM messages (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),
    
    -- Routing
    source string,           -- 'telegram', 'whatsapp', 'slack', 'agent', 'skill', 'system'
    target string,           -- 'agent', 'channel:telegram', 'skill:weather', 'broadcast'
    session_id string,       -- Groups related messages
    
    -- Content
    message_type string,     -- 'user_input', 'agent_response', 'tool_call', 'tool_result', 'error'
    content string,          -- JSON payload
    
    -- Metadata
    user_id string,
    channel_metadata string, -- Channel-specific data (JSON)
    priority int8 DEFAULT 0  -- -1: low, 0: normal, 1: high, 2: urgent
) 
SETTINGS event_time_column='timestamp';

-- Index for fast session lookups
CREATE MATERIALIZED VIEW messages_by_session AS
SELECT * FROM messages
ORDER BY session_id, timestamp;
```

### 3.2 LLM Observability Stream

Every LLM interaction is logged for debugging, cost tracking, and analysis:

```sql
CREATE STREAM llm_logs (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),
    
    -- Request
    session_id string,
    model string,               -- 'claude-opus-4-5', 'gpt-4o', 'deepseek-r1'
    provider string,            -- 'anthropic', 'openai', 'openrouter'
    
    -- Tokens & Cost
    input_tokens int32,
    output_tokens int32,
    total_tokens int32,
    estimated_cost_usd float32,
    
    -- Timing
    latency_ms int32,
    time_to_first_token_ms int32,
    
    -- Content (for debugging)
    system_prompt_hash string,  -- SHA256 of system prompt (not full content)
    user_message_preview string,-- First 200 chars
    assistant_response_preview string,
    
    -- Tool Usage
    tools_called array(string),
    tool_call_count int8,
    
    -- Status
    status string,              -- 'success', 'error', 'rate_limited', 'timeout'
    error_message string
)
SETTINGS event_time_column='timestamp';

-- Real-time cost monitoring view
CREATE MATERIALIZED VIEW llm_cost_hourly AS
SELECT 
    tumble_start(timestamp, 1h) as hour,
    model,
    count() as request_count,
    sum(total_tokens) as total_tokens,
    sum(estimated_cost_usd) as total_cost_usd,
    avg(latency_ms) as avg_latency_ms
FROM llm_logs
GROUP BY hour, model;
```

### 3.3 Memory Stream (Agent Knowledge Base)

Persistent memory with vector search capability:

```sql
CREATE STREAM memory (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),
    
    -- Classification
    memory_type string,         -- 'fact', 'preference', 'conversation_summary', 'skill_learned'
    category string,            -- 'user_info', 'project', 'schedule', 'general'
    
    -- Content
    content string,             -- The memory itself
    source_session_id string,   -- Where this memory originated
    
    -- Vector embedding for semantic search
    embedding array(float32),   -- 1536-dim for OpenAI, 1024 for others
    
    -- Lifecycle
    importance float32,         -- 0.0 to 1.0, affects retrieval priority
    access_count int32 DEFAULT 0,
    last_accessed datetime64(3),
    expires_at datetime64(3)    -- Optional TTL
)
SETTINGS event_time_column='timestamp';

-- Vector search index (Timeplus/ClickHouse native)
ALTER STREAM memory ADD INDEX memory_vector_idx embedding TYPE vector_similarity('hnsw', 'cosineDistance');
```

### 3.4 Events Stream (System Events & Triggers)

```sql
CREATE STREAM events (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),
    
    event_type string,          -- 'heartbeat', 'channel_connected', 'skill_loaded', 'error', 'alert'
    source string,
    severity string,            -- 'debug', 'info', 'warning', 'error', 'critical'
    
    payload string,             -- JSON event data
    
    -- For filtering
    tags array(string)
)
SETTINGS event_time_column='timestamp';
```

### 3.5 External Data Streams

Templates for ingesting external data sources:

```sql
-- Market Data (example)
CREATE EXTERNAL STREAM market_data (
    symbol string,
    price float64,
    volume int64,
    timestamp datetime64(3)
)
SETTINGS 
    type='kafka',
    brokers='kafka.example.com:9092',
    topic='market_data',
    data_format='JSONEachRow';

-- News Feed (example)  
CREATE EXTERNAL STREAM news_feed (
    title string,
    content string,
    source string,
    published_at datetime64(3),
    categories array(string)
)
SETTINGS
    type='kafka',
    brokers='kafka.example.com:9092',
    topic='news_events',
    data_format='JSONEachRow';
```

---

## 4\. Scheduled Tasks (Replacing Cron/Heartbeat)

Timeplus Tasks replace traditional cron jobs with SQL-native scheduling:

### 4.1 Heartbeat Task

```sql
-- Proactive check-in every 30 minutes
CREATE TASK heartbeat_task
SCHEDULE 30m
TIMEOUT 10s
INTO messages
AS
SELECT
    uuid() as id,
    now64(3) as timestamp,
    'system' as source,
    'agent' as target,
    uuid() as session_id,
    'heartbeat' as message_type,
    to_json_string(map(
        'action', 'proactive_check',
        'checks', ['calendar', 'email', 'reminders']
    )) as content,
    'system' as user_id,
    '' as channel_metadata,
    0 as priority;
```

### 4.2 Daily Summary Task

```sql
CREATE TASK daily_summary
SCHEDULE CRON '0 9 * * *'  -- 9 AM daily
TIMEOUT 60s
INTO messages
AS
SELECT
    uuid() as id,
    now64(3) as timestamp,
    'system' as source,
    'agent' as target,
    uuid() as session_id,
    'scheduled_task' as message_type,
    to_json_string(map(
        'action', 'generate_daily_briefing',
        'include', ['calendar', 'weather', 'news', 'reminders']
    )) as content,
    'system' as user_id,
    '' as channel_metadata,
    1 as priority;
```

### 4.3 Cost Alert Task

```sql
CREATE TASK cost_alert
SCHEDULE 1h
TIMEOUT 5s
INTO events
AS
SELECT
    uuid() as id,
    now64(3) as timestamp,
    'cost_alert' as event_type,
    'llm_monitor' as source,
    if(hourly_cost > 5.0, 'warning', 'info') as severity,
    to_json_string(map(
        'hourly_cost_usd', hourly_cost,
        'request_count', req_count
    )) as payload,
    ['cost', 'llm'] as tags
FROM (
    SELECT 
        sum(estimated_cost_usd) as hourly_cost,
        count() as req_count
    FROM table(llm_logs)
    WHERE timestamp > now() - interval 1 hour
);
```

---

## 5\. Python Backend Architecture

### 5.1 Project Structure

```
PulseBot/
├── __init__.py
├── main.py                 # Entry point, CLI
├── config.py               # Configuration management
│
├── core/                   # ~800 lines
│   ├── __init__.py
│   ├── agent.py            # Main agent loop
│   ├── router.py           # Message routing logic
│   ├── context.py          # Prompt/context builder
│   └── executor.py         # Tool execution engine
│
├── timeplus/               # ~600 lines
│   ├── __init__.py
│   ├── client.py           # Timeplus connection wrapper
│   ├── streams.py          # Stream operations (read/write)
│   ├── tasks.py            # Task management
│   └── memory.py           # Memory operations with vector search
│
├── providers/              # ~500 lines
│   ├── __init__.py
│   ├── base.py             # LLM provider interface
│   ├── anthropic.py        # Claude integration
│   ├── openai.py           # OpenAI/OpenRouter integration
│   └── ollama.py           # Local model support
│
├── channels/               # ~800 lines
│   ├── __init__.py
│   ├── base.py             # Channel interface
│   ├── telegram.py         # Telegram bot
│   ├── whatsapp.py         # WhatsApp (via whatsapp-web.js bridge)
│   ├── slack.py            # Slack integration
│   └── webchat.py          # Built-in web interface
│
├── skills/                 # ~600 lines
│   ├── __init__.py
│   ├── base.py             # Skill interface
│   ├── builtin/
│   │   ├── web_search.py   # Web search tool
│   │   ├── file_ops.py     # File operations
│   │   ├── shell.py        # Shell command execution
│   │   └── browser.py      # Browser automation
│   └── loader.py           # Dynamic skill loading
│
├── mcp/                    # ~400 lines
│   ├── __init__.py
│   ├── client.py           # MCP protocol client
│   └── registry.py         # MCP server registry
│
├── db/                     # ~300 lines
│   ├── __init__.py
│   ├── postgres.py         # PostgreSQL operations
│   └── models.py           # SQLAlchemy models
│
├── api/                    # ~500 lines
│   ├── __init__.py
│   ├── routes.py           # FastAPI routes
│   └── websocket.py        # WebSocket for real-time updates
│
└── utils/                  # ~300 lines
    ├── __init__.py
    ├── logging.py          # Structured logging
    └── helpers.py          # Utility functions

# Total: ~4,800 lines
```

### 5.2 Core Agent Loop

```py
# core/agent.py
import asyncio
import json
from typing import AsyncIterator
from datetime import datetime

from timeplus.client import TimeplusClient
from timeplus.streams import StreamReader, StreamWriter
from providers.base import LLMProvider
from core.context import ContextBuilder
from core.executor import ToolExecutor
from skills.loader import SkillLoader


class Agent:
    """
    The main agent loop that:
    1. Listens to the messages stream for incoming requests
    2. Builds context from memory and conversation history
    3. Calls LLM for reasoning
    4. Executes tools and writes results back to stream
    """
    
    def __init__(
        self,
        agent_id: str,
        timeplus: TimeplusClient,
        llm_provider: LLMProvider,
        skill_loader: SkillLoader,
    ):
        self.agent_id = agent_id
        self.tp = timeplus
        self.llm = llm_provider
        self.skills = skill_loader
        
        self.context_builder = ContextBuilder(timeplus)
        self.executor = ToolExecutor(skill_loader)
        
        self.messages_reader = StreamReader(timeplus, "messages")
        self.messages_writer = StreamWriter(timeplus, "messages")
        self.llm_logger = StreamWriter(timeplus, "llm_logs")
    
    async def run(self):
        """Main event loop - listen for messages targeting this agent"""
        query = f"""
            SELECT * FROM messages 
            WHERE target = 'agent' 
              AND message_type IN ('user_input', 'tool_result', 'heartbeat', 'scheduled_task')
            SETTINGS seek_to='latest'
        """
        
        async for message in self.messages_reader.stream(query):
            try:
                await self._process_message(message)
            except Exception as e:
                await self._log_error(message, e)
    
    async def _process_message(self, message: dict):
        """Process a single incoming message through the agent loop"""
        session_id = message["session_id"]
        message_type = message["message_type"]
        content = json.loads(message["content"])
        
        # Build context from memory + recent conversation
        context = await self.context_builder.build(
            session_id=session_id,
            user_message=content.get("text", ""),
            include_memory=True,
            memory_limit=10,
        )
        
        # Get available tools from loaded skills
        tools = self.skills.get_tool_definitions()
        
        # Agent loop: keep calling LLM until no more tool calls
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call LLM
            start_time = datetime.now()
            response = await self.llm.chat(
                messages=context.messages,
                tools=tools,
                system=context.system_prompt,
            )
            latency_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            # Log to observability stream
            await self._log_llm_call(session_id, response, latency_ms)
            
            # Check if LLM wants to call tools
            if response.tool_calls:
                # Execute tools
                for tool_call in response.tool_calls:
                    result = await self.executor.execute(
                        tool_name=tool_call.name,
                        arguments=tool_call.arguments,
                        session_id=session_id,
                    )
                    
                    # Add tool result to context for next iteration
                    context.add_tool_result(tool_call.id, result)
            else:
                # No tool calls - send final response
                await self._send_response(
                    session_id=session_id,
                    source_message=message,
                    response_text=response.content,
                )
                
                # Extract and store any new memories
                await self._extract_memories(session_id, context, response)
                break
    
    async def _send_response(self, session_id: str, source_message: dict, response_text: str):
        """Write agent response back to the messages stream"""
        await self.messages_writer.write({
            "source": "agent",
            "target": f"channel:{source_message.get('source', 'webchat')}",
            "session_id": session_id,
            "message_type": "agent_response",
            "content": json.dumps({"text": response_text}),
            "user_id": source_message.get("user_id", ""),
            "channel_metadata": source_message.get("channel_metadata", ""),
            "priority": 0,
        })
    
    async def _log_llm_call(self, session_id: str, response, latency_ms: float):
        """Log LLM call to observability stream"""
        await self.llm_logger.write({
            "session_id": session_id,
            "model": self.llm.model,
            "provider": self.llm.provider_name,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
            "estimated_cost_usd": self._estimate_cost(response.usage),
            "latency_ms": int(latency_ms),
            "tools_called": [tc.name for tc in (response.tool_calls or [])],
            "tool_call_count": len(response.tool_calls or []),
            "status": "success",
        })
    
    async def _extract_memories(self, session_id: str, context, response):
        """Extract important information to store as memories"""
        # Use LLM to identify memorable facts from the conversation
        memory_prompt = """
        Review this conversation and extract any important facts, preferences, 
        or information worth remembering about the user. Return as JSON array:
        [{"type": "fact|preference|reminder", "content": "...", "importance": 0.0-1.0}]
        Return empty array if nothing worth remembering.
        """
        
        extraction = await self.llm.chat(
            messages=[{"role": "user", "content": memory_prompt + str(context.messages[-5:])}],
            system="You are a memory extraction assistant. Be concise.",
        )
        
        try:
            memories = json.loads(extraction.content)
            for mem in memories:
                await self.tp.memory.store(
                    content=mem["content"],
                    memory_type=mem["type"],
                    importance=mem.get("importance", 0.5),
                    source_session_id=session_id,
                )
        except json.JSONDecodeError:
            pass  # No valid memories extracted
```

### 5.3 Timeplus Client Wrapper

```py
# timeplus/client.py
import asyncio
from typing import AsyncIterator, Optional, List, Dict, Any
import timeplus_connect
from timeplus_connect import get_client


class TimeplusClient:
    """
    Wrapper around timeplus-connect for both batch and streaming queries.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8123,
        streaming_port: int = 3218,
        username: str = "default",
        password: str = "",
    ):
        self.host = host
        self.port = port
        self.streaming_port = streaming_port
        self.username = username
        self.password = password
        
        # Batch client (for writes and historical queries)
        self.batch_client = get_client(
            host=host,
            port=port,
            username=username,
            password=password,
        )
        
        # Streaming client (for real-time queries)
        self.stream_client = get_client(
            host=host,
            port=streaming_port,
            username=username,
            password=password,
        )
        
        # Initialize sub-modules
        self.memory = MemoryManager(self)
    
    def execute(self, query: str) -> Any:
        """Execute a batch query (DDL, INSERT, historical SELECT)"""
        return self.batch_client.command(query)
    
    def query(self, query: str) -> List[Dict]:
        """Execute a historical query and return results"""
        result = self.batch_client.query(query)
        return [dict(zip(result.column_names, row)) for row in result.result_rows]
    
    def insert(self, stream: str, data: List[Dict], column_names: Optional[List[str]] = None):
        """Insert data into a stream"""
        if not data:
            return
        
        if column_names is None:
            column_names = list(data[0].keys())
        
        rows = [[row.get(col) for col in column_names] for row in data]
        self.batch_client.insert(stream, rows, column_names=column_names)
    
    async def stream_query(self, query: str) -> AsyncIterator[Dict]:
        """
        Execute a streaming query and yield results as they arrive.
        Uses the streaming port (3218) for unbounded queries.
        """
        # Use arrow stream for efficient streaming
        with self.stream_client.query_arrow_stream(query) as stream:
            for batch in stream:
                df = batch.to_pandas()
                for _, row in df.iterrows():
                    yield row.to_dict()


class MemoryManager:
    """Memory operations with vector search support"""
    
    def __init__(self, client: TimeplusClient):
        self.client = client
        self._embedding_model = None
    
    async def store(
        self,
        content: str,
        memory_type: str,
        importance: float = 0.5,
        source_session_id: str = "",
        category: str = "general",
    ):
        """Store a memory with its embedding"""
        embedding = await self._get_embedding(content)
        
        self.client.insert("memory", [{
            "memory_type": memory_type,
            "category": category,
            "content": content,
            "source_session_id": source_session_id,
            "embedding": embedding,
            "importance": importance,
        }])
    
    async def search(
        self,
        query: str,
        limit: int = 5,
        min_importance: float = 0.0,
    ) -> List[Dict]:
        """Semantic search over memories using vector similarity"""
        query_embedding = await self._get_embedding(query)
        
        # Hybrid search: vector similarity + importance weighting
        sql = f"""
            SELECT 
                id,
                content,
                memory_type,
                category,
                importance,
                cosineDistance(embedding, {query_embedding}) as distance,
                (1 - cosineDistance(embedding, {query_embedding})) * importance as score
            FROM table(memory)
            WHERE importance >= {min_importance}
            ORDER BY score DESC
            LIMIT {limit}
        """
        
        return self.client.query(sql)
    
    async def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text (uses OpenAI by default)"""
        # Lazy load embedding model
        if self._embedding_model is None:
            from openai import OpenAI
            self._embedding_model = OpenAI()
        
        response = self._embedding_model.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding
```

### 5.4 Stream Reader/Writer

```py
# timeplus/streams.py
import asyncio
import json
from typing import AsyncIterator, Dict, Any, Optional
from datetime import datetime


class StreamReader:
    """Async stream reader for real-time message consumption"""
    
    def __init__(self, client, stream_name: str):
        self.client = client
        self.stream_name = stream_name
    
    async def stream(
        self,
        query: Optional[str] = None,
        seek_to: str = "latest",
    ) -> AsyncIterator[Dict]:
        """
        Stream messages from Timeplus.
        
        Args:
            query: Custom SQL query. If None, selects all from stream.
            seek_to: 'latest', 'earliest', or timestamp
        """
        if query is None:
            query = f"SELECT * FROM {self.stream_name} SETTINGS seek_to='{seek_to}'"
        
        async for row in self.client.stream_query(query):
            yield row
    
    async def read_history(
        self,
        session_id: Optional[str] = None,
        limit: int = 100,
        since: Optional[datetime] = None,
    ) -> list[Dict]:
        """Read historical messages (batch query)"""
        conditions = []
        
        if session_id:
            conditions.append(f"session_id = '{session_id}'")
        if since:
            conditions.append(f"timestamp >= '{since.isoformat()}'")
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        query = f"""
            SELECT * FROM table({self.stream_name})
            {where_clause}
            ORDER BY timestamp DESC
            LIMIT {limit}
        """
        
        return self.client.query(query)


class StreamWriter:
    """Stream writer for publishing messages"""
    
    def __init__(self, client, stream_name: str):
        self.client = client
        self.stream_name = stream_name
    
    async def write(self, data: Dict[str, Any]):
        """Write a single message to the stream"""
        # Ensure required fields have defaults
        data.setdefault("id", str(uuid.uuid4()))
        data.setdefault("timestamp", datetime.now())
        
        self.client.insert(self.stream_name, [data])
    
    async def write_batch(self, data: list[Dict[str, Any]]):
        """Write multiple messages efficiently"""
        for item in data:
            item.setdefault("id", str(uuid.uuid4()))
            item.setdefault("timestamp", datetime.now())
        
        self.client.insert(self.stream_name, data)
```

### 5.5 Channel Interface (Example: Telegram)

```py
# channels/telegram.py
import asyncio
import json
from typing import Optional
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from channels.base import BaseChannel
from timeplus.streams import StreamWriter, StreamReader


class TelegramChannel(BaseChannel):
    """Telegram bot channel integration"""
    
    name = "telegram"
    
    def __init__(self, config: dict, timeplus_client):
        self.token = config["token"]
        self.allowed_users = config.get("allowFrom", [])
        
        self.tp = timeplus_client
        self.writer = StreamWriter(timeplus_client, "messages")
        self.reader = StreamReader(timeplus_client, "messages")
        
        self.app = Application.builder().token(self.token).build()
        self.bot: Optional[Bot] = None
    
    async def start(self):
        """Start the Telegram bot and response listener"""
        # Register message handler
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        )
        
        # Start bot
        await self.app.initialize()
        await self.app.start()
        self.bot = self.app.bot
        
        # Start listening for agent responses
        asyncio.create_task(self._listen_for_responses())
        
        # Start polling
        await self.app.updater.start_polling()
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming Telegram message"""
        user_id = str(update.effective_user.id)
        
        # Check if user is allowed
        if self.allowed_users and user_id not in self.allowed_users:
            await update.message.reply_text("Sorry, you're not authorized to use this bot.")
            return
        
        # Generate session ID (persistent per user)
        session_id = f"telegram:{user_id}"
        
        # Write to messages stream
        await self.writer.write({
            "source": "telegram",
            "target": "agent",
            "session_id": session_id,
            "message_type": "user_input",
            "content": json.dumps({
                "text": update.message.text,
                "chat_id": update.effective_chat.id,
                "message_id": update.message.message_id,
            }),
            "user_id": user_id,
            "channel_metadata": json.dumps({
                "chat_id": update.effective_chat.id,
                "username": update.effective_user.username,
            }),
        })
    
    async def _listen_for_responses(self):
        """Listen for agent responses targeting this channel"""
        query = """
            SELECT * FROM messages
            WHERE target = 'channel:telegram'
              AND message_type = 'agent_response'
            SETTINGS seek_to='latest'
        """
        
        async for message in self.reader.stream(query):
            await self._send_response(message)
    
    async def _send_response(self, message: dict):
        """Send response back to Telegram"""
        content = json.loads(message["content"])
        metadata = json.loads(message.get("channel_metadata", "{}"))
        
        chat_id = metadata.get("chat_id")
        if chat_id and self.bot:
            await self.bot.send_message(
                chat_id=chat_id,
                text=content.get("text", ""),
                parse_mode="Markdown",
            )
    
    async def stop(self):
        """Stop the channel"""
        if self.app.updater:
            await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
```

### 5.6 Skill Interface

```py
# skills/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ToolDefinition(BaseModel):
    """OpenAI-compatible tool definition"""
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema


class ToolResult(BaseModel):
    """Result from tool execution"""
    success: bool
    output: Any
    error: Optional[str] = None


class BaseSkill(ABC):
    """Base class for all skills (tools)"""
    
    name: str
    description: str
    
    @abstractmethod
    def get_tools(self) -> List[ToolDefinition]:
        """Return list of tools provided by this skill"""
        pass
    
    @abstractmethod
    async def execute(self, tool_name: str, arguments: Dict[str, Any]) -> ToolResult:
        """Execute a tool with given arguments"""
        pass


# skills/builtin/web_search.py
import aiohttp
from skills.base import BaseSkill, ToolDefinition, ToolResult


class WebSearchSkill(BaseSkill):
    """Web search using Brave Search API"""
    
    name = "web_search"
    description = "Search the web for current information"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
    
    def get_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="web_search",
                description="Search the web for current information, news, or facts",
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
    
    async def execute(self, tool_name: str, arguments: dict) -> ToolResult:
        if tool_name != "web_search":
            return ToolResult(success=False, output=None, error=f"Unknown tool: {tool_name}")
        
        query = arguments.get("query", "")
        count = min(arguments.get("count", 5), 10)
        
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url,
                headers=headers,
                params={"q": query, "count": count}
            ) as response:
                if response.status != 200:
                    return ToolResult(
                        success=False,
                        output=None,
                        error=f"Search failed: {response.status}"
                    )
                
                data = await response.json()
                results = []
                
                for item in data.get("web", {}).get("results", []):
                    results.append({
                        "title": item.get("title"),
                        "url": item.get("url"),
                        "description": item.get("description"),
                    })
                
                return ToolResult(success=True, output=results)
```

---

## 6\. PostgreSQL Schema (Metadata Storage)

```sql
-- Agents configuration
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    model VARCHAR(255) NOT NULL DEFAULT 'claude-opus-4-5',
    provider VARCHAR(50) NOT NULL DEFAULT 'anthropic',
    system_prompt TEXT,
    temperature FLOAT DEFAULT 0.7,
    max_tokens INT DEFAULT 4096,
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Skills registry
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    module_path VARCHAR(500) NOT NULL,  -- Python module path
    config JSONB DEFAULT '{}',
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Agent-Skill mapping
CREATE TABLE agent_skills (
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
    config_override JSONB DEFAULT '{}',
    PRIMARY KEY (agent_id, skill_id)
);

-- Channel configurations
CREATE TABLE channels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,  -- 'telegram', 'slack', etc.
    config JSONB NOT NULL,  -- Channel-specific config (encrypted sensitive fields)
    agent_id UUID REFERENCES agents(id),
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- MCP Server registry
CREATE TABLE mcp_servers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,
    transport VARCHAR(50) DEFAULT 'stdio',  -- 'stdio', 'http', 'ws'
    config JSONB DEFAULT '{}',
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Scheduled tasks (mirrors Timeplus tasks for UI management)
CREATE TABLE scheduled_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    schedule VARCHAR(100) NOT NULL,  -- Cron expression or interval
    task_type VARCHAR(50) NOT NULL,  -- 'heartbeat', 'summary', 'custom'
    payload JSONB DEFAULT '{}',
    enabled BOOLEAN DEFAULT true,
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User sessions (for identity linking across channels)
CREATE TABLE user_identities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_id VARCHAR(255) NOT NULL,  -- Unified user ID
    channel VARCHAR(100) NOT NULL,
    channel_user_id VARCHAR(255) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(channel, channel_user_id)
);
```

---

## 7\. React Frontend Architecture

### 7.1 Project Structure

```
frontend/
├── src/
│   ├── index.js
│   ├── App.js
│   │
│   ├── components/
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.jsx       # Main dashboard
│   │   │   ├── StreamMonitor.jsx   # Real-time stream viewer
│   │   │   ├── CostTracker.jsx     # LLM cost analytics
│   │   │   └── EventLog.jsx        # System events
│   │   │
│   │   ├── Chat/
│   │   │   ├── ChatInterface.jsx   # Web chat UI
│   │   │   ├── MessageList.jsx
│   │   │   └── MessageInput.jsx
│   │   │
│   │   ├── Config/
│   │   │   ├── AgentConfig.jsx     # Agent settings
│   │   │   ├── ChannelConfig.jsx   # Channel management
│   │   │   ├── SkillConfig.jsx     # Skills management
│   │   │   └── TaskConfig.jsx      # Scheduled tasks
│   │   │
│   │   └── Analytics/
│   │       ├── Analytics.jsx       # Analytics dashboard
│   │       ├── TokenUsage.jsx      # Token/cost charts
│   │       └── MemoryBrowser.jsx   # Memory search UI
│   │
│   ├── hooks/
│   │   ├── useWebSocket.js         # WebSocket connection
│   │   ├── useStream.js            # Stream data subscription
│   │   └── useApi.js               # REST API calls
│   │
│   ├── services/
│   │   ├── api.js                  # API client
│   │   └── websocket.js            # WebSocket client
│   │
│   └── styles/
│       └── main.css
│
├── package.json
└── vite.config.js
```

### 7.2 Real-time Stream Monitor Component

```
// components/Dashboard/StreamMonitor.jsx
import React, { useState, useEffect, useRef } from 'react';
import { useWebSocket } from '../../hooks/useWebSocket';

const StreamMonitor = ({ streamName = 'messages' }) => {
  const [messages, setMessages] = useState([]);
  const [filter, setFilter] = useState('');
  const messagesEndRef = useRef(null);
  
  // Connect to WebSocket for real-time updates
  const { lastMessage, connectionStatus } = useWebSocket(
    `ws://localhost:8000/ws/stream/${streamName}`
  );
  
  useEffect(() => {
    if (lastMessage) {
      setMessages(prev => [...prev.slice(-99), lastMessage]);
    }
  }, [lastMessage]);
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const filteredMessages = messages.filter(msg => 
    !filter || JSON.stringify(msg).toLowerCase().includes(filter.toLowerCase())
  );
  
  return (
    <div className="stream-monitor">
      <div className="stream-header">
        <h3>📡 Stream: {streamName}</h3>
        <span className={`status ${connectionStatus}`}>
          {connectionStatus}
        </span>
      </div>
      
      <input
        type="text"
        placeholder="Filter messages..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        className="filter-input"
      />
      
      <div className="messages-container">
        {filteredMessages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.message_type}`}>
            <div className="message-header">
              <span className="source">{msg.source}</span>
              <span className="arrow">→</span>
              <span className="target">{msg.target}</span>
              <span className="timestamp">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <pre className="message-content">
              {JSON.stringify(JSON.parse(msg.content || '{}'), null, 2)}
            </pre>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default StreamMonitor;
```

### 7.3 Cost Tracker Component

```
// components/Dashboard/CostTracker.jsx
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useApi } from '../../hooks/useApi';

const CostTracker = () => {
  const [timeRange, setTimeRange] = useState('24h');
  const [costData, setCostData] = useState([]);
  const [summary, setSummary] = useState(null);
  
  const api = useApi();
  
  useEffect(() => {
    const fetchCostData = async () => {
      // Query the llm_cost_hourly materialized view
      const response = await api.get(`/analytics/costs?range=${timeRange}`);
      setCostData(response.data.hourly);
      setSummary(response.data.summary);
    };
    
    fetchCostData();
    const interval = setInterval(fetchCostData, 60000); // Refresh every minute
    
    return () => clearInterval(interval);
  }, [timeRange]);
  
  return (
    <div className="cost-tracker">
      <div className="tracker-header">
        <h3>💰 LLM Cost Tracker</h3>
        <select value={timeRange} onChange={(e) => setTimeRange(e.target.value)}>
          <option value="1h">Last Hour</option>
          <option value="24h">Last 24 Hours</option>
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
        </select>
      </div>
      
      {summary && (
        <div className="summary-cards">
          <div className="card">
            <span className="label">Total Cost</span>
            <span className="value">${summary.total_cost_usd.toFixed(2)}</span>
          </div>
          <div className="card">
            <span className="label">Total Tokens</span>
            <span className="value">{(summary.total_tokens / 1000).toFixed(1)}K</span>
          </div>
          <div className="card">
            <span className="label">Requests</span>
            <span className="value">{summary.total_requests}</span>
          </div>
          <div className="card">
            <span className="label">Avg Latency</span>
            <span className="value">{summary.avg_latency_ms.toFixed(0)}ms</span>
          </div>
        </div>
      )}
      
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={costData}>
            <XAxis 
              dataKey="hour" 
              tickFormatter={(v) => new Date(v).toLocaleTimeString()}
            />
            <YAxis />
            <Tooltip 
              formatter={(value) => [`$${value.toFixed(3)}`, 'Cost']}
              labelFormatter={(v) => new Date(v).toLocaleString()}
            />
            <Line 
              type="monotone" 
              dataKey="total_cost_usd" 
              stroke="#8884d8" 
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default CostTracker;
```

---

## 8\. System Prompt Template

Based on OpenClaw's proven approach, here's the recommended system prompt structure:

```py
# core/prompts.py

SYSTEM_PROMPT_TEMPLATE = """
You are {agent_name}, a helpful AI assistant powered by PulseBot.

## Core Identity
{custom_identity}

## Current Context
- Current time: {current_time}
- User: {user_name}
- Session: {session_id}
- Channel: {channel_name}

## Available Tools
You have access to the following tools:
{tools_list}

## Relevant Memories
{memories}

## Guidelines

### Tool Usage
- Use tools proactively when they can help answer questions or complete tasks
- Always explain what you're doing before calling a tool
- If a tool fails, explain the error and try an alternative approach
- Chain multiple tools when needed to complete complex tasks

### Communication Style
- Be concise but thorough
- Use markdown formatting when helpful
- Ask clarifying questions if the request is ambiguous
- Confirm before taking irreversible actions (file deletion, sending messages, etc.)

### Memory
- I will remember important facts, preferences, and context from our conversations
- You can ask me to remember or forget specific things
- I proactively use relevant memories to personalize responses

### Limitations
- I cannot access the internet in real-time without the web_search tool
- I cannot execute code unless the shell tool is enabled
- I respect user privacy and will not share session information

{custom_instructions}
"""

def build_system_prompt(
    agent_name: str,
    custom_identity: str,
    tools: list,
    memories: list,
    user_name: str,
    session_id: str,
    channel_name: str,
    custom_instructions: str = "",
) -> str:
    """Build the complete system prompt"""
    
    # Format tools list
    tools_list = "\n".join([
        f"- **{t.name}**: {t.description}"
        for t in tools
    ])
    
    # Format memories
    memories_text = "\n".join([
        f"- [{m['memory_type']}] {m['content']}"
        for m in memories
    ]) if memories else "No relevant memories found."
    
    return SYSTEM_PROMPT_TEMPLATE.format(
        agent_name=agent_name,
        custom_identity=custom_identity,
        current_time=datetime.now().isoformat(),
        user_name=user_name,
        session_id=session_id,
        channel_name=channel_name,
        tools_list=tools_list,
        memories=memories_text,
        custom_instructions=custom_instructions,
    )
```

---

## 9\. MCP Integration

```py
# mcp/client.py
import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class MCPTool:
    name: str
    description: str
    input_schema: Dict[str, Any]


class MCPClient:
    """
    Model Context Protocol client for connecting to external tool servers.
    Supports stdio, HTTP, and WebSocket transports.
    """
    
    def __init__(self, server_config: dict):
        self.name = server_config["name"]
        self.transport = server_config.get("transport", "stdio")
        self.url = server_config.get("url")
        self.command = server_config.get("command")
        self.args = server_config.get("args", [])
        
        self._process: Optional[asyncio.subprocess.Process] = None
        self._tools: List[MCPTool] = []
    
    async def connect(self):
        """Initialize connection to MCP server"""
        if self.transport == "stdio":
            await self._connect_stdio()
        elif self.transport == "http":
            await self._connect_http()
        else:
            raise ValueError(f"Unsupported transport: {self.transport}")
        
        # Discover available tools
        await self._discover_tools()
    
    async def _connect_stdio(self):
        """Connect via stdio (spawn subprocess)"""
        self._process = await asyncio.create_subprocess_exec(
            self.command,
            *self.args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    
    async def _discover_tools(self):
        """Request tool list from MCP server"""
        response = await self._send_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
        })
        
        self._tools = [
            MCPTool(
                name=t["name"],
                description=t.get("description", ""),
                input_schema=t.get("inputSchema", {}),
            )
            for t in response.get("result", {}).get("tools", [])
        ]
    
    def get_tools(self) -> List[MCPTool]:
        """Return available tools"""
        return self._tools
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool on the MCP server"""
        response = await self._send_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments,
            }
        })
        
        return response.get("result", {}).get("content", [])
    
    async def _send_request(self, request: dict) -> dict:
        """Send JSON-RPC request to server"""
        if self.transport == "stdio" and self._process:
            # Write request
            request_bytes = (json.dumps(request) + "\n").encode()
            self._process.stdin.write(request_bytes)
            await self._process.stdin.drain()
            
            # Read response
            response_line = await self._process.stdout.readline()
            return json.loads(response_line.decode())
        
        raise RuntimeError("Not connected")
    
    async def disconnect(self):
        """Close connection"""
        if self._process:
            self._process.terminate()
            await self._process.wait()
```

---

## 10\. Deployment Configuration

### 10.1 Docker Compose

```
# docker-compose.yml
version: '3.8'

services:
  # Timeplus Proton (Streaming SQL Engine)
  proton:
    image: d.timeplus.com/timeplus-io/proton:latest
    ports:
      - "8123:8123"   # HTTP (batch queries)
      - "3218:3218"   # HTTP (streaming queries)
      - "8463:8463"   # Native protocol
    volumes:
      - proton_data:/var/lib/proton
    environment:
      - PROTON_MAX_MEMORY_USAGE_RATIO=0.8
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8123/ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # PostgreSQL (Metadata)
  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: PulseBot
      POSTGRES_USER: PulseBot
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql

  # PulseBot Backend
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - TIMEPLUS_HOST=proton
      - TIMEPLUS_PORT=8123
      - TIMEPLUS_STREAMING_PORT=3218
      - POSTGRES_HOST=postgres
      - POSTGRES_DB=PulseBot
      - POSTGRES_USER=PulseBot
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-changeme}
      - LLM_PROVIDER=${LLM_PROVIDER:-anthropic}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      proton:
        condition: service_healthy
      postgres:
        condition: service_started
    volumes:
      - ./skills:/app/skills  # Mount custom skills

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - REACT_APP_WS_URL=ws://localhost:8000
    depends_on:
      - backend

  # WhatsApp Bridge (optional)
  whatsapp-bridge:
    build:
      context: ./bridge/whatsapp
      dockerfile: Dockerfile
    volumes:
      - whatsapp_auth:/app/.wwebjs_auth
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
    profiles:
      - whatsapp

volumes:
  proton_data:
  postgres_data:
  whatsapp_auth:
```

### 10.2 Configuration File

```
# config.yaml
agent:
  name: "PulseBot"
  model: "claude-opus-4-5"
  provider: "anthropic"
  temperature: 0.7
  max_tokens: 4096

timeplus:
  host: "localhost"
  port: 8123
  streaming_port: 3218
  username: "default"
  password: ""

postgres:
  host: "localhost"
  port: 5432
  database: "PulseBot"
  username: "PulseBot"
  password: ""

providers:
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    default_model: "claude-opus-4-5"
  
  openai:
    api_key: "${OPENAI_API_KEY}"
    default_model: "gpt-4o"
  
  openrouter:
    api_key: "${OPENROUTER_API_KEY}"
    default_model: "anthropic/claude-opus-4-5"

channels:
  telegram:
    enabled: true
    token: "${TELEGRAM_BOT_TOKEN}"
    allow_from:
      - "123456789"  # Telegram user IDs
  
  slack:
    enabled: false
    bot_token: "${SLACK_BOT_TOKEN}"
    app_token: "${SLACK_APP_TOKEN}"
  
  webchat:
    enabled: true
    port: 8000

skills:
  builtin:
    - web_search
    - file_ops
    - shell
    - browser
  
  custom: []

mcp_servers:
  - name: "filesystem"
    transport: "stdio"
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"]

scheduled_tasks:
  heartbeat:
    enabled: true
    interval: "30m"
    actions: ["calendar", "reminders"]
  
  daily_summary:
    enabled: true
    cron: "0 9 * * *"
    timezone: "America/Vancouver"
```

---

## 11\. CLI Interface

```py
# cli/main.py
import click
import asyncio
from rich.console import Console
from rich.table import Table

from PulseBot.core.agent import Agent
from PulseBot.config import load_config


console = Console()


@click.group()
def cli():
    """PulseBot - Stream-Native AI Agent"""
    pass


@cli.command()
def init():
    """Initialize PulseBot configuration and streams"""
    console.print("[bold green]Initializing PulseBot...[/bold green]")
    
    # Create Timeplus streams
    from PulseBot.timeplus.setup import create_streams
    asyncio.run(create_streams())
    
    # Create PostgreSQL tables
    from PulseBot.db.setup import create_tables
    asyncio.run(create_tables())
    
    # Generate default config
    from PulseBot.config import generate_default_config
    generate_default_config()
    
    console.print("[bold green]✓ Initialization complete![/bold green]")


@cli.command()
@click.option('--config', '-c', default='config.yaml', help='Config file path')
def start(config):
    """Start the PulseBot gateway"""
    console.print(f"[bold blue]Starting PulseBot with {config}...[/bold blue]")
    
    cfg = load_config(config)
    
    from PulseBot.gateway import Gateway
    gateway = Gateway(cfg)
    asyncio.run(gateway.run())


@cli.command()
@click.option('--message', '-m', required=True, help='Message to send')
@click.option('--model', default=None, help='Override model')
def chat(message, model):
    """Chat with the agent directly"""
    from PulseBot.core.agent import quick_chat
    
    response = asyncio.run(quick_chat(message, model=model))
    console.print(f"\n[bold cyan]Agent:[/bold cyan] {response}\n")


@cli.command()
def status():
    """Show PulseBot status"""
    from PulseBot.status import get_status
    
    status = asyncio.run(get_status())
    
    table = Table(title="PulseBot Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details")
    
    for component, info in status.items():
        table.add_row(
            component,
            "✓" if info["healthy"] else "✗",
            info.get("details", "")
        )
    
    console.print(table)


@cli.group()
def channels():
    """Manage channels"""
    pass


@channels.command(name='list')
def list_channels():
    """List configured channels"""
    from PulseBot.channels import get_channels
    
    channels = asyncio.run(get_channels())
    
    table = Table(title="Channels")
    table.add_column("Name")
    table.add_column("Enabled")
    table.add_column("Status")
    
    for ch in channels:
        table.add_row(ch["name"], str(ch["enabled"]), ch["status"])
    
    console.print(table)


@cli.group()
def tasks():
    """Manage scheduled tasks"""
    pass


@tasks.command(name='list')
def list_tasks():
    """List scheduled tasks"""
    pass


@tasks.command(name='add')
@click.option('--name', required=True)
@click.option('--schedule', required=True, help='Cron expression or interval (e.g., "30m", "0 9 * * *")')
@click.option('--action', required=True)
def add_task(name, schedule, action):
    """Add a scheduled task"""
    pass


if __name__ == '__main__':
    cli()
```

---

## 12\. Comparison: PulseBot vs OpenClaw vs Nanobot

| Feature | OpenClaw | Nanobot | PulseBot |
| :---- | :---- | :---- | :---- |
| **Codebase Size** | \~430K lines (TypeScript) | \~4K lines (Python) | \~5K lines (Python) |
| **Language** | TypeScript/Node.js | Python | Python |
| **Memory System** | Markdown files \+ SQLite | JSON files | Timeplus Streams \+ Vector Search |
| **Scheduling** | Node.js cron | APScheduler | Timeplus Tasks (SQL-native) |
| **Observability** | JSONL logs | Basic logging | Real-time streams \+ dashboards |
| **Communication** | WebSocket \+ file locks | Direct function calls | Timeplus message streams |
| **Setup Complexity** | High (45+ min) | Low (\~5 min) | Medium (\~10 min) |
| **GUI** | Control UI (optional) | None | React dashboard (included) |
| **Scalability** | Single node | Single node | Distributed (Timeplus) |
| **Cost Tracking** | Manual estimation | None | Real-time SQL analytics |

---

## 14\. Conclusion

PulseBot delivers a powerful, observable, and extensible AI agent by leveraging Timeplus's streaming SQL engine as the backbone for all inter-component communication, scheduling, and analytics. The stream-native architecture provides:

1. **Simplicity**: \~5K lines of Python vs 430K lines for OpenClaw  
2. **Observability**: Every event flows through queryable streams  
3. **Scalability**: Timeplus handles millions of events per second  
4. **SQL-First**: Non-developers can query and extend via SQL  
5. **Real-time**: Sub-second message routing and analytics

This architecture positions PulseBot as the lightweight, enterprise-ready alternative to OpenClaw, purpose-built for teams who value observability and SQL-native workflows.  
