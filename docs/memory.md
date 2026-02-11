# PulseBot Memory System

## Overview

PulseBot implements a sophisticated memory system that enables the agent to remember important information across conversations. The system uses **vector embeddings** and **semantic search** to retrieve relevant memories based on the current context, providing a more personalized and context-aware experience.

### Key Features

- **Vector-Based Semantic Search**: Uses configurable embedding providers (OpenAI or Ollama) to find memories semantically similar to the current query
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
    embedding array(float32), -- Variable dimensions based on embedding provider
    
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
from pulsebot.embeddings import OpenAIEmbeddingProvider

# Initialize with OpenAI embeddings
client = TimeplusClient(host="localhost", port=8463)
embedding_provider = OpenAIEmbeddingProvider(
    api_key="sk-...",
    model="text-embedding-3-small"
)
memory = MemoryManager(
    client=client,
    embedding_provider=embedding_provider,
    stream_name="memory",
    similarity_threshold=0.95,  # Adjust sensitivity (0.0-1.0)
)
```

### Embedding Providers (`pulsebot/embeddings/`)

PulseBot supports multiple embedding providers:

#### OpenAI Embedding Provider

Uses OpenAI's embedding API. Supports models:
- `text-embedding-3-small` (1536 dimensions) - Default
- `text-embedding-3-large` (3072 dimensions)
- `text-embedding-ada-002` (1536 dimensions)

```python
from pulsebot.embeddings import OpenAIEmbeddingProvider

provider = OpenAIEmbeddingProvider(
    api_key="sk-...",
    model="text-embedding-3-small"
)
```

#### Ollama Embedding Provider

Uses local Ollama models for embeddings. Supports models:
- `mxbai-embed-large` (1024 dimensions)
- `all-minilm` (384 dimensions)
- `nomic-embed-text` (768 dimensions)
- `bge-large` (1024 dimensions)

```python
from pulsebot.embeddings import OllamaEmbeddingProvider

provider = OllamaEmbeddingProvider(
    host="http://localhost:11434",
    model="mxbai-embed-large"
)

# Dimensions are auto-detected on first use
# Or specify explicitly:
provider = OllamaEmbeddingProvider(
    host="http://localhost:11434",
    model="all-minilm",
    dimensions=384
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
    check_duplicates: bool = True,
) -> str:
    """Store a memory and return its ID.
    
    Automatically checks for duplicates using semantic similarity.
    If a very similar memory exists, returns the existing ID instead
    of storing a duplicate.
    """
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

**Duplicate Detection**

The memory system automatically prevents duplicate storage using semantic similarity:

- **Pure Similarity Scoring**: Uses cosine similarity (not hybrid) for duplicate detection to focus on content similarity
- **Configurable Threshold**: Default 0.95 for very strict duplicate detection
- **Cross-Type Search**: Searches across all memory types/categories to prevent conceptual duplicates
- **Near-Duplicate Monitoring**: Logs near-duplicates for threshold tuning
- **Smart Storage**: Returns existing memory ID instead of creating duplicates

```python
# Store first occurrence
id1 = await memory.store("User's name is John Smith", check_duplicates=True)

# Store duplicate - returns same ID
id2 = await memory.store("User's name is John Smith", check_duplicates=True)
assert id1 == id2  # Same ID returned

# Store similar but different content
id3 = await memory.store("User name is John Smith", check_duplicates=True)
# Different ID if similarity < threshold

# Store with different importance - still detected as duplicate
id4 = await memory.store("User's name is John Smith", importance=0.9, check_duplicates=True)
assert id4 == id1  # Same ID returned regardless of importance
```

**Advanced Deduplication Features:**
- **Hybrid vs Pure Similarity**: Uses pure cosine similarity for deduplication (content-focused) vs hybrid scoring for retrieval (importance-weighted)
- **Near-Duplicate Detection**: Logs memories with 80%+ of threshold similarity for monitoring
- **Flexible Filtering**: Optional memory type/category filtering for targeted deduplication

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
        logger.info("Memory manager not available - skipping extraction")
        return
    
    if not self.memory.is_available():
        logger.info("Memory features not available - skipping extraction")
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
- User personal information (name, contact details, role, company)
- User preferences (communication style, interests, settings, favorite tools)
- Important facts (projects they're working on, technical expertise)
- Scheduled reminders or commitments
- Learned information that could help future interactions

Examples of good extractions:
- {"type": "fact", "content": "User's name is John Smith", "importance": 0.9}
- {"type": "preference", "content": "User prefers Python over Java", "importance": 0.7}
- {"type": "fact", "content": "User works at Acme Corp as Data Scientist", "importance": 0.8}

Do NOT extract:
- Generic pleasantries or greetings
- Transient information
- Information already known/obvious
- Questions the user asked (unless they reveal preferences)
"""
```

## Configuration

### Environment Variables

```bash
# For OpenAI embeddings
OPENAI_API_KEY=sk-...

# For Ollama embeddings
OLLAMA_HOST=http://localhost:11434
```

### Config YAML

Memory system and embedding providers are now configured together in the memory section:

```yaml
# Memory system configuration (includes embedding settings)
memory:
  similarity_threshold: 0.95  # Adjust duplicate detection sensitivity (0.0-1.0)
  enabled: true
  
  # Embedding provider configuration for memory operations
  embedding_provider: "openai"  # or "ollama"
  embedding_model: "text-embedding-3-small"  # OpenAI: text-embedding-3-small (1536), text-embedding-3-large (3072)
                                              # Ollama: mxbai-embed-large (1024), all-minilm (384), nomic-embed-text (768)
  # embedding_api_key: "${OPENAI_API_KEY}"     # Optional: override OpenAI API key
  # embedding_host: "${OLLAMA_HOST}"           # Optional: override Ollama host
  # embedding_dimensions: 1536                 # Optional: auto-detected if not set
  embedding_timeout_seconds: 30

# LLM providers (separate from memory/embedding)
providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    default_model: "gpt-4o"
  
  ollama:
    enabled: true
    host: "${OLLAMA_HOST:-http://localhost:11434}"
    default_model: "llama3"
```

**Memory Configuration Options:**

- **`similarity_threshold`**: Controls how strict duplicate detection is (0.0-1.0)
  - `0.95` (Default): Very strict - only obvious duplicates skipped
  - `0.90`: Moderate - similar concepts considered duplicates  
  - `0.85`: Loose - broader concept matching
  - `0.80`: Very loose - catches most related memories

- **`enabled`**: Enable/disable the entire memory system

**Embedding Configuration Options:**

- **`embedding_provider`**: `"openai"` or `"ollama"`
- **`embedding_model`**: Model name for embeddings
- **`embedding_api_key`**: Optional override for OpenAI API key
- **`embedding_host`**: Optional override for Ollama host
- **`embedding_dimensions`**: Optional manual dimensions (auto-detected if not set)
- **`embedding_timeout_seconds`**: Request timeout (default: 30)

### Programmatic Usage

```python
from pulsebot.timeplus.memory import MemoryManager
from pulsebot.timeplus.client import TimeplusClient
from pulsebot.config import load_config
from pulsebot.embeddings import OpenAIEmbeddingProvider, OllamaEmbeddingProvider

config = load_config("config.yaml")
client = TimeplusClient.from_config(config.timeplus)

# Initialize embedding provider based on memory configuration
memory_cfg = config.memory
if memory_cfg.embedding_provider == "openai":
    embedding_provider = OpenAIEmbeddingProvider(
        api_key=memory_cfg.embedding_api_key or config.providers.openai.api_key,
        model=memory_cfg.embedding_model,
        dimensions=memory_cfg.embedding_dimensions,
    )
elif memory_cfg.embedding_provider == "ollama":
    embedding_provider = OllamaEmbeddingProvider(
        host=memory_cfg.embedding_host or config.providers.ollama.host,
        model=memory_cfg.embedding_model,
        dimensions=memory_cfg.embedding_dimensions,
        timeout_seconds=memory_cfg.embedding_timeout_seconds,
    )

# Initialize memory manager with separate client to avoid connection conflicts
memory_client = TimeplusClient.from_config(config.timeplus)
memory = MemoryManager(
    client=memory_client,
    embedding_provider=embedding_provider,
    similarity_threshold=memory_cfg.similarity_threshold,
)

# Check if available and enabled
if memory.is_available() and memory_cfg.enabled:
    # Use memory features
    results = await memory.search("user preferences")
```

### Configuration-Based Initialization

The memory system can be completely disabled or configured via `config.yaml`:

```yaml
memory:
  similarity_threshold: 0.95  # Duplicate detection sensitivity
  enabled: true               # Enable/disable memory system
  
  # Embedding provider configuration
  embedding_provider: "openai"  # or "ollama"
  embedding_model: "text-embedding-3-small"
  # embedding_api_key: "${OPENAI_API_KEY}"  # Optional override
  # embedding_host: "${OLLAMA_HOST}"        # Optional override
  # embedding_dimensions: 1536              # Optional manual dimensions
  embedding_timeout_seconds: 30
```

### Duplicate Detection Configuration

The memory system uses semantic similarity to prevent duplicate storage:

**Similarity Thresholds:**
- **0.95** (Default): Very strict - only obvious duplicates skipped
- **0.90**: Moderate - similar concepts considered duplicates  
- **0.85**: Loose - broader concept matching
- **0.80**: Very loose - catches most related memories

**Recommendations:**
- Start with default (0.95) to avoid false positives
- Lower threshold if you want aggressive deduplication
- Higher threshold if legitimate memories are being skipped
- Monitor logs to tune the setting appropriately

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

### Duplicate Prevention

- **Enable duplicate checking** for all memory storage operations
- **Monitor similarity scores** in logs to tune thresholds
- **Watch for near-duplicates** in debug logs to optimize threshold settings
- **Use appropriate thresholds** based on your use case:
  - High precision (0.95+): For factual information
  - Moderate (0.90): For general preferences
  - Lower (0.85): For broad conceptual memories
- **Consider content structure** - consistent formatting reduces false duplicates
- **Review duplicate stats** periodically using `get_duplicate_stats()` method

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

- **Cause**: No embedding provider configured or provider unavailable
- **Solution**: 
  - For OpenAI: Set `OPENAI_API_KEY` environment variable
  - For Ollama: Ensure Ollama is running and configured in `config.yaml`

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

- Embedding generation requires API call to embedding provider
- Consider caching frequently accessed memories
- Use more specific queries to reduce results

## Advanced Topics

### Custom Embedding Models

You can use different embedding models by specifying the model name:

```python
memory = MemoryManager(
    client=client,
    embedding_provider=openai_provider,  # or ollama_provider
)
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

## Connection Management

### Separate Clients for Concurrent Operations

To avoid "Simultaneous queries on single connection" errors, PulseBot uses separate Timeplus clients:

```python
# In pulsebot/cli.py
tp = TimeplusClient.from_config(cfg.timeplus)           # Main streaming client
memory_tp = TimeplusClient.from_config(cfg.timeplus)    # Memory operations client

memory = MemoryManager(
    client=memory_tp,           # Separate client for memory
    embedding_provider=embedding_provider,
)
```

This ensures that:
- Long-running streaming queries don't block memory operations
- Memory searches use historical queries (`client.query()`)
- All operations can run concurrently without connection conflicts

## Custom Embedding Providers

You can create custom embedding providers by implementing the `EmbeddingProvider` interface:

```python
from pulsebot.embeddings.base import EmbeddingProvider

class CustomEmbeddingProvider(EmbeddingProvider):
    """Custom embedding provider implementation."""
    
    provider_name = "custom"
    model = "my-model"
    dimensions = 768
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client = None
    
    async def embed(self, text: str) -> list[float]:
        """Generate embedding for text."""
        # Implementation here
        return [0.0] * self.dimensions
    
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        return [await self.embed(text) for text in texts]
```

## Dimension Compatibility

When switching embedding providers, be aware of dimension differences:

| Provider | Model | Dimensions |
|----------|-------|------------|
| OpenAI | text-embedding-3-small | 1536 |
| OpenAI | text-embedding-3-large | 3072 |
| OpenAI | text-embedding-ada-002 | 1536 |
| Ollama | mxbai-embed-large | 1024 |
| Ollama | all-minilm | 384 |
| Ollama | nomic-embed-text | 768 |
| Ollama | bge-large | 1024 |

**Note**: Mixing embeddings with different dimensions will cause errors. When switching providers, you may need to clear existing memories or ensure all stored memories use the same embedding model.

## Summary

PulseBot's memory system provides:

1. **Semantic Retrieval**: Vector-based search finds conceptually similar memories
2. **Hybrid Scoring**: Combines similarity and importance for relevance ranking
3. **Automatic Extraction**: LLM extracts memories from conversations automatically
4. **Type Classification**: Organized by memory type and category
5. **Stream-Native**: All data flows through Timeplus streams
6. **Soft Deletes**: Append-only with deletion support
7. **Flexible Queries**: Filter by type, category, importance, or session
8. **Multiple Providers**: Support for OpenAI (cloud) and Ollama (local) embeddings
9. **Auto-Detection**: Automatically detects embedding dimensions for Ollama models
10. **Connection Safety**: Uses separate clients to prevent query conflicts
11. **Intelligent Deduplication**: Automatic semantic deduplication prevents memory explosion
12. **Pure Similarity Focus**: Uses cosine similarity (not hybrid) for content-focused duplicate detection
13. **Near-Duplicate Monitoring**: Logs similar memories for threshold optimization
14. **Configurable Sensitivity**: Adjustable similarity thresholds for precise control

To enable memory, configure an embedding provider in `config.yaml`:
- **OpenAI**: Set `OPENAI_API_KEY` environment variable
- **Ollama**: Configure `providers.embedding.provider = "ollama"` with appropriate host and model

The agent will automatically remember and recall relevant information to provide personalized responses, while preventing duplicate storage through advanced semantic deduplication that focuses on content similarity rather than importance-weighted retrieval scores.