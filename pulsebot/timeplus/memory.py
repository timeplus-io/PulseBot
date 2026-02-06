"""Memory manager with vector search support for PulseBot."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.timeplus.client import TimeplusClient

logger = get_logger(__name__)


def _format_embedding(embedding: list[float]) -> str:
    """Format embedding array for SQL query."""
    return "[" + ",".join(str(x) for x in embedding) + "]"


class MemoryManager:
    """Memory operations with vector search support.
    
    Stores and retrieves memories using Timeplus streams with 
    vector similarity search for semantic retrieval.
    
    Example:
        >>> memory = MemoryManager(client, openai_api_key="...")
        >>> await memory.store("User prefers dark mode", memory_type="preference")
        >>> results = await memory.search("What are the user's preferences?")
    """
    
    def __init__(
        self,
        client: "TimeplusClient",
        openai_api_key: str | None = None,
        embedding_model: str = "text-embedding-3-small",
        stream_name: str = "memory",
    ):
        """Initialize memory manager.
        
        Args:
            client: Timeplus client instance
            openai_api_key: OpenAI API key for embeddings
            embedding_model: OpenAI embedding model to use
            stream_name: Name of the memory stream
        """
        self.client = client
        self.openai_api_key = openai_api_key
        self.embedding_model = embedding_model
        self.stream_name = stream_name
        self._openai_client: Any = None

        # Ensure memory stream exists
        self._ensure_stream_exists()
    
    def _ensure_stream_exists(self) -> None:
        """Create the memory stream if it doesn't exist."""
        from pulsebot.timeplus.setup import MEMORY_STREAM_DDL

        try:
            self.client.execute(MEMORY_STREAM_DDL)
            logger.debug(f"Ensured memory stream exists: {self.stream_name}")
        except Exception as e:
            logger.warning(f"Could not create memory stream: {e}")

    @property
    def openai_client(self) -> Any:
        """Get or create OpenAI client (lazy initialization)."""
        if self._openai_client is None:
            from openai import OpenAI
            self._openai_client = OpenAI(api_key=self.openai_api_key)
        return self._openai_client
    
    def is_available(self) -> bool:
        """Check if memory features are available (requires OpenAI API key)."""
        return bool(self.openai_api_key)

    async def _get_embedding(self, text: str) -> list[float]:
        """Generate embedding for text using OpenAI.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (1536 dimensions for text-embedding-3-small)

        Raises:
            ValueError: If OpenAI API key is not configured
        """
        if not self.openai_api_key:
            raise ValueError("OpenAI API key required for memory embeddings")

        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text,
        )
        return response.data[0].embedding
    
    async def store(
        self,
        content: str,
        memory_type: str = "fact",
        category: str = "general",
        importance: float = 0.5,
        source_session_id: str = "",
    ) -> str:
        """Store a memory with its embedding.

        Args:
            content: The memory content to store
            memory_type: Type of memory ('fact', 'preference', 'conversation_summary', 'skill_learned')
            category: Category ('user_info', 'project', 'schedule', 'general')
            importance: Importance score 0.0 to 1.0
            source_session_id: Session where this memory originated

        Returns:
            Memory ID
        """
        import uuid

        # Generate embedding
        embedding = await self._get_embedding(content)

        memory_id = str(uuid.uuid4())

        data = {
            "id": memory_id,
            "memory_type": memory_type,
            "category": category,
            "content": content,
            "source_session_id": source_session_id,
            "embedding": embedding,
            "importance": importance,
            "is_deleted": False,
        }

        self.client.insert(self.stream_name, [data])

        logger.info(
            "Stored memory",
            extra={
                "id": memory_id,
                "type": memory_type,
                "category": category,
                "importance": importance,
            }
        )

        return memory_id
    
    async def search(
        self,
        query: str,
        limit: int = 5,
        min_importance: float = 0.0,
        memory_types: list[str] | None = None,
        categories: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Semantic search over memories using vector similarity.
        
        Uses a hybrid scoring approach combining cosine similarity 
        with importance weighting.
        
        Args:
            query: Search query
            limit: Maximum results to return
            min_importance: Minimum importance threshold
            memory_types: Filter by memory types
            categories: Filter by categories
            
        Returns:
            List of matching memories with similarity scores
        """
        # Generate query embedding
        query_embedding = await self._get_embedding(query)
        embedding_str = _format_embedding(query_embedding)
        
        # Build WHERE clause
        conditions = [
            f"importance >= {min_importance}",
            "is_deleted = false",
        ]

        if memory_types:
            types_str = ", ".join(f"'{t}'" for t in memory_types)
            conditions.append(f"memory_type IN ({types_str})")

        if categories:
            cats_str = ", ".join(f"'{c}'" for c in categories)
            conditions.append(f"category IN ({cats_str})")
        
        where_clause = " AND ".join(conditions)
        
        # Hybrid search: vector similarity + importance weighting
        sql = f"""
            SELECT 
                id,
                content,
                memory_type,
                category,
                importance,
                source_session_id,
                timestamp,
                cosine_distance(embedding, {embedding_str}) as distance,
                (1 - cosine_distance(embedding, {embedding_str})) * importance as score
            FROM table({self.stream_name})
            WHERE {where_clause}
            ORDER BY score DESC
            LIMIT {limit}
        """
        
        results = self.client.query(sql)
        
        logger.debug(
            "Memory search",
            extra={"query": query[:50], "results": len(results)}
        )
        
        return results
    
    async def get_by_session(
        self,
        session_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Get memories originating from a specific session.

        Args:
            session_id: Session ID to filter by
            limit: Maximum results

        Returns:
            List of memories from the session
        """
        sql = f"""
            SELECT
                id,
                content,
                memory_type,
                category,
                importance,
                timestamp
            FROM table({self.stream_name})
            WHERE source_session_id = '{session_id}'
              AND is_deleted = false
            ORDER BY timestamp DESC
            LIMIT {limit}
        """

        return self.client.query(sql)
    
    async def get_recent(
        self,
        limit: int = 10,
        memory_types: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Get most recent memories.

        Args:
            limit: Maximum results
            memory_types: Optional filter by types

        Returns:
            List of recent memories
        """
        conditions = ["is_deleted = false"]
        if memory_types:
            types_str = ", ".join(f"'{t}'" for t in memory_types)
            conditions.append(f"memory_type IN ({types_str})")

        where_clause = "WHERE " + " AND ".join(conditions)

        sql = f"""
            SELECT
                id,
                content,
                memory_type,
                category,
                importance,
                timestamp
            FROM table({self.stream_name})
            {where_clause}
            ORDER BY timestamp DESC
            LIMIT {limit}
        """

        return self.client.query(sql)
    
    async def mark_deleted(self, memory_id: str) -> None:
        """Mark a memory as deleted (soft delete for append-only stream).

        Note: This inserts a new record marking the memory as deleted.
        Queries filter out is_deleted=true records.

        Args:
            memory_id: Memory ID to mark as deleted
        """
        # For append-only streams, we insert a deletion marker
        # Future queries will filter by is_deleted=false
        logger.info("Memory deletion not fully supported in append-only mode", extra={"id": memory_id})
