# PulseBot Memory System

## Overview

PulseBot implements a sophisticated memory system that enables the agent to remember important information across conversations. The system uses **vector embeddings** and **semantic search** to retrieve relevant memories based on the current context, providing a more personalized and context-aware experience.

### Key Features

- **Vector-Based Semantic Search**: Uses OpenAI embeddings to find memories semantically similar to the current query
- **Hybrid Scoring**: Combines cosine similarity with importance weighting for better relevance
- **Automatic Memory Extraction**: LLM automatically extracts important facts from conversations
- **Memory Classification**: Memories are categorized by type (fact, preference, conversation_summary, skill_learned)
- **Soft Deletes**: Append-only stream with soft delete support
- **Timeplus Integration**: All memories stored in Timeplus streams for persistence and observability

## Architecture

### Memory Stream Schema

The `memory` stream stores all memories with the following schema (defined in `pulsebot/timeplus/setup.py`):

```sql
CREATE STREAM IF NOT EXISTS memory (
    id string DEFAULT uuid(),
    timestamp datetime64(3) DEFAULT now64(3),
    
    -- Classification
    memory_type string,  -- 'fact', 'preference', 'conversation_summary', 'skill_learned'
    category string,     -- 'user_info', 'project', 'schedule', 'general'
    
    -- Content
    content string,           -- The memory itself
    source_session_id string, -- Where this memory originated
    
    -- Vector embedding for semantic search
    embedding array(float32), -- 1536-dim for OpenAI text-embedding-3-small
    
    -- Lifecycle
    importance float32,       -- 0.0 to 1.0, affects retrieval priority
    is_deleted bool DEFAULT false  -- Soft delete flag
)
```

### Memory Types

| Type | Description | Example |
|------|-------------|---------|
| `fact` | Factual information | "User works at Timeplus" |
| `preference` | User preferences | "User prefers Python over JavaScript" |
| `conversation_summary` | Summaries of past conversations | "Discussed database architecture" |
| `skill_learned` | Skills the agent learned | "Learned to use custom API" |

### Categories

| Category | Description |
|----------|-------------|
| `user_info` | Personal information about the user |
| `project` | Project-specific information |
| `schedule` | Time-related information, reminders |
| `general` | General facts and preferences |

## Components

### MemoryManager (`pulsebot/timeplus/memory.py`)

The core class that manages all memory operations.

```python
from pulsebot.timeplus.memory import MemoryManager
from pulsebot.timeplus.client import TimeplusClient

# Initialize
client = TimeplusClient(host="localhost", port=8463)
memory = MemoryManager(
    client=client,
    openai_api_key="sk-...",  # Required for embeddings
    embedding_model="text-embedding-3-small",
    stream_name="memory"
)
```

#### Key Methods

**Storing Memories**

```python
async def store(
    self,
    content: str,
    memory_type: str = "fact",
    category: str = "general",
    importance: float = 0.5,
    source_session_id: str = "",
) -> str:
    """Store a memory and return its ID."""
```

Example:
```python
memory_id = await memory.store(
    content="User prefers dark mode in all applications",
    memory_type="preference",
    category="user_info",
    importance=0.8,
    source_session_id="session-abc123"
)
```

**Semantic Search**

Uses a hybrid scoring approach: `(1 - cosine_distance) * importance`

```python
async def search(
    self,
    query: str,
    limit: int = 5,
    min_importance: float = 0.0,
    memory_types: list[str] | None = None,
    categories: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Search memories using vector similarity."""
```

Example:
```python
results = await memory.search(
    query="What are the user's UI preferences?",
    limit=5,
    memory_types=["preference"],
    min_importance=0.5
)

for mem in results:
    print(f"[{mem['memory_type']}] {mem['content']} (score: {mem['score']})")
```

**Retrieving by Session**

```python
memories = await memory.get_by_session(
    session_id="session-abc123",
    limit=20
)
```

**Getting Recent Memories**

```python
recent = await memory.get_recent(
    limit=10,
    memory_types=["fact", "preference"]
)
```

**Soft Delete**

```python
await memory.mark_deleted(memory_id)
```

Note: Since Timeplus streams are append-only, deletion inserts a new record. Future queries filter out `is_deleted=true` records.

## How Memory Works

### 1. Context Building

When processing a user message, the agent builds a context that includes relevant memories:

```
User Message → ContextBuilder
                    ↓
            Memory Search (Vector Similarity)
                    ↓
            Relevant Memories → System Prompt
                    ↓
            LLM with Contextual Memory
```

**In `pulsebot/core/context.py`:**

```python
async def build(
    self,
    session_id: str,
    user_message: str,
    include_memory: bool = True,
    memory_limit: int = 10,
    ...
) -> Context:
    # Fetch relevant memories via semantic search
    memories = []
    if include_memory and self.memory and user_message and self.memory.is_available():
        memories = await self._get_relevant_memories(user_message, memory_limit)
    
    # Build system prompt with memories
    system_prompt = build_system_prompt(
        ...
        memories=memories,
        ...
    )
    ...
```

### 2. Memory Retrieval Flow

```python
async def _get_relevant_memories(self, query: str, limit: int):
    # 1. Generate embedding for current query
    query_embedding = await self._get_embedding(query)
    
    # 2. Search using cosine distance + importance weighting
    sql = f"""
    SELECT 
        id, content, memory_type, category, importance,
        cosine_distance(embedding, {embedding_str}) as distance,
        (1 - cosine_distance(embedding, {embedding_str})) * importance as score
    FROM table(memory)
    WHERE importance >= {min_importance} AND is_deleted = false
    ORDER BY score DESC
    LIMIT {limit}
    """
    
    return self.client.query(sql)
```

### 3. Memory in System Prompt

Relevant memories are formatted and included in the system prompt (`pulsebot/core/prompts.py`):

```python
SYSTEM_PROMPT_TEMPLATE = """
...

## Relevant Memories
{memories}

## Guidelines
...
### Memory
- I will remember important facts, preferences, and context from our conversations
- You can ask me to remember or forget specific things
- I proactively use relevant memories to personalize responses
...
"""

def build_system_prompt(..., memories: list[dict], ...):
    if memories:
        memories_text = "\n".join([
            f"- [{m.get('memory_type', 'fact')}] {m.get('content', '')}"
            for m in memories
        ])
    else:
        memories_text = "No relevant memories found."
    
    return SYSTEM_PROMPT_TEMPLATE.format(
        ...
        memories=memories_text,
        ...
    )
```

### 4. Automatic Memory Extraction

After each conversation turn, the agent automatically extracts memories to store:

```
User Query → Agent Process → LLM Response
                                    ↓
                            Memory Extraction
                                    ↓
                            Store to Memory Stream
```

**In `pulsebot/core/agent.py`:**

```python
async def _extract_memories(
    self,
    session_id: str,
    context: Any,
    response: Any,
) -> None:
    if not self.memory:
        return
    
    # Get last 5 messages
    recent_messages = context.messages[-5:]
    
    # Use LLM to extract memories
    extraction_prompt = build_memory_extraction_prompt()
    extraction = await self.llm.chat(
        messages=[{
            "role": "user",
            "content": extraction_prompt + "\n\nConversation:\n" + json.dumps(recent_messages),
        }],
        system="You are a memory extraction assistant. Be concise. Return only valid JSON.",
    )
    
    # Parse and store memories
    memories = json.loads(extraction.content)
    for mem in memories:
        if isinstance(mem, dict) and "content" in mem:
            await self.memory.store(
                content=mem["content"],
                memory_type=mem.get("type", "fact"),
                importance=mem.get("importance", 0.5),
                source_session_id=session_id,
            )
```

**Memory Extraction Prompt** (`pulsebot/core/prompts.py`):

```python
def build_memory_extraction_prompt() -> str:
    return """
Review this conversation and extract any important facts, preferences,
or information worth remembering about the user. Return as JSON array:
[{"type": "fact|preference|reminder", "content": "...", "importance": 0.0-1.0}]

Return empty array [] if nothing worth remembering.

Be selective - only extract genuinely useful information like:
- User preferences (communication style, interests, settings)
- Important facts (name, location, projects they're working on)
- Scheduled reminders or commitments
- Learned information that could help future interactions

Do NOT extract:
- Generic pleasantries or greetings
- Transient information
- Information already known/obvious
"""
```

## Configuration

### Environment Variables

```bash
# Required for memory embeddings
OPENAI_API_KEY=sk-...

# Optional: Custom embedding model
MEMORY_EMBEDDING_MODEL=text-embedding-3-small
```

### Config YAML

Memory is enabled automatically when `OPENAI_API_KEY` is available:

```yaml
providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    embedding_model: "text-embedding-3-small"
```

### Programmatic Usage

```python
from pulsebot.timeplus.memory import MemoryManager
from pulsebot.timeplus.client import TimeplusClient
from pulsebot.config import load_config

config = load_config("config.yaml")
client = TimeplusClient.from_config(config.timeplus)

# Initialize memory manager
memory = MemoryManager(
    client=client,
    openai_api_key=config.providers.openai.api_key,
    embedding_model=config.providers.openai.embedding_model or "text-embedding-3-small"
)

# Check if available
if memory.is_available():
    # Use memory features
    results = await memory.search("user preferences")
```

## Querying Memories Directly

You can query the memory stream directly using Timeplus SQL:

### Basic Queries

```sql
-- Get all memories
SELECT * FROM table(memory) WHERE is_deleted = false

-- Get recent memories
SELECT * FROM table(memory) 
WHERE is_deleted = false 
ORDER BY timestamp DESC 
LIMIT 10

-- Get memories by type
SELECT * FROM table(memory) 
WHERE memory_type = 'preference' AND is_deleted = false

-- Get memories by session
SELECT * FROM table(memory) 
WHERE source_session_id = 'session-abc123'
```

### Vector Search Queries

```sql
-- Search with embedding (replace with actual embedding array)
SELECT 
    id,
    content,
    memory_type,
    importance,
    cosine_distance(embedding, [0.1, 0.2, ...]) as distance,
    (1 - cosine_distance(embedding, [0.1, 0.2, ...])) * importance as score
FROM table(memory)
WHERE is_deleted = false AND importance >= 0.5
ORDER BY score DESC
LIMIT 5
```

## Best Practices

### Importance Scoring

- **0.0-0.3**: Low importance, transient information
- **0.3-0.6**: Medium importance, general preferences
- **0.6-0.8**: High importance, key facts about user
- **0.8-1.0**: Critical information, must remember

### Memory Types

Choose appropriate types to improve retrieval:

- Use `fact` for objective information
- Use `preference` for subjective choices
- Use `conversation_summary` for context from past discussions
- Use `skill_learned` for new capabilities

### Categories

Categorize memories for better organization:

- `user_info`: Personal details (name, role, preferences)
- `project`: Work-related context
- `schedule`: Time-based information, reminders
- `general`: Everything else

### Privacy Considerations

- Memories persist across sessions
- Use `is_deleted` for GDPR compliance
- Consider data retention policies
- Don't store sensitive information (passwords, tokens)

## Debugging Memory

### Enable Debug Logging

```python
import logging
logging.getLogger("pulsebot.timeplus.memory").setLevel(logging.DEBUG)
```

### Check Memory Usage

```python
# Get memory stats
recent = await memory.get_recent(limit=100)
print(f"Total memories: {len(recent)}")

# Check by type
types = {}
for mem in recent:
    t = mem.get('memory_type', 'unknown')
    types[t] = types.get(t, 0) + 1
print(f"By type: {types}")
```

### Query from Timeplus CLI

```bash
# Connect to Timeplus
timeplusd client --user proton --password timeplus@t+

# Query memories
proton> SELECT memory_type, category, content, importance 
        FROM table(memory) 
        WHERE is_deleted = false 
        ORDER BY timestamp DESC 
        LIMIT 10;
```

## Troubleshooting

### "Memory features not available"

- **Cause**: `OPENAI_API_KEY` not configured
- **Solution**: Set the environment variable or pass to MemoryManager

### Memories not being retrieved

1. Check if `memory.is_available()` returns `True`
2. Verify the `memory` stream exists in Timeplus
3. Check if memories are being stored (look for "Stored memory" logs)
4. Verify embedding generation is working

### Search returns no results

- Memories may have low importance (default 0.5)
- Check `min_importance` parameter
- Verify memories are not marked as deleted
- Ensure query is semantically similar to stored content

### High latency on memory operations

- Embedding generation requires API call to OpenAI
- Consider caching frequently accessed memories
- Use more specific queries to reduce results

## Advanced Topics

### Custom Embedding Models

You can use different embedding models by specifying the model name:

```python
memory = MemoryManager(
    client=client,
    openai_api_key="sk-...",
    embedding_model="text-embedding-3-large"  # 3072 dimensions
)
```

**Note**: If changing dimensions, update the stream schema:

```sql
-- Drop and recreate with new dimension
DROP STREAM IF EXISTS memory;
CREATE STREAM memory (
    ...
    embedding array(float32),  -- Update size if needed
    ...
);
```

### Memory Backup and Migration

Export memories:

```python
all_memories = await memory.get_recent(limit=10000)
import json
with open("memories_backup.json", "w") as f:
    json.dump(all_memories, f, indent=2)
```

Import memories:

```python
with open("memories_backup.json") as f:
    memories = json.load(f)

for mem in memories:
    await memory.store(
        content=mem["content"],
        memory_type=mem["memory_type"],
        category=mem["category"],
        importance=mem["importance"],
        source_session_id=mem["source_session_id"],
    )
```

### Integration with Context Builder

The ContextBuilder automatically includes memories when building prompts:

```python
from pulsebot.core.context import ContextBuilder

builder = ContextBuilder(
    timeplus_client=client,
    memory_manager=memory,
    agent_name="MyBot",
)

context = await builder.build(
    session_id="abc123",
    user_message="What's my name?",
    include_memory=True,      # Enable memory retrieval
    memory_limit=10,          # Max memories to include
)
```

## Summary

PulseBot's memory system provides:

1. **Semantic Retrieval**: Vector-based search finds conceptually similar memories
2. **Hybrid Scoring**: Combines similarity and importance for relevance ranking
3. **Automatic Extraction**: LLM extracts memories from conversations automatically
4. **Type Classification**: Organized by memory type and category
5. **Stream-Native**: All data flows through Timeplus streams
6. **Soft Deletes**: Append-only with deletion support
7. **Flexible Queries**: Filter by type, category, importance, or session

To enable memory, simply configure `OPENAI_API_KEY` and the agent will automatically remember and recall relevant information to provide personalized responses.
