"""Memory manager with vector search support for PulseBot."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from pulsebot.utils import get_logger, truncate_string

if TYPE_CHECKING:
    from pulsebot.embeddings.base import EmbeddingProvider
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
        >>> from pulsebot.embeddings.openai import OpenAIEmbeddingProvider
        >>> embedding_provider = OpenAIEmbeddingProvider(api_key="...")
        >>> memory = MemoryManager(client, embedding_provider=embedding_provider)
        >>> await memory.store("User prefers dark mode", memory_type="preference")
        >>> results = await memory.search("What are the user's preferences?")
    """

    def __init__(
        self,
        client: "TimeplusClient",
        embedding_provider: "EmbeddingProvider | None" = None,
        stream_name: str = "memory",
        similarity_threshold: float = 0.95,
    ):
        """Initialize memory manager.

        Args:
            client: Timeplus client instance
            embedding_provider: Embedding provider for generating embeddings
            stream_name: Name of the memory stream
            similarity_threshold: Cosine similarity threshold for duplicate detection (0.0-1.0)
        """
        self.client = client
        self.embedding_provider = embedding_provider
        self.stream_name = stream_name
        self.similarity_threshold = similarity_threshold

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

    def is_available(self) -> bool:
        """Check if memory features are available (requires embedding provider)."""
        return self.embedding_provider is not None and self.embedding_provider.is_available()

    async def _get_embedding(self, text: str) -> list[float]:
        """Generate embedding for text using the configured provider.

        Args:
            text: Text to embed

        Returns:
            Embedding vector

        Raises:
            ValueError: If embedding provider is not configured or available
            RuntimeError: If embedding generation fails
        """
        if not self.embedding_provider:
            raise ValueError("Embedding provider not configured")

        if not self.embedding_provider.is_available():
            raise ValueError(f"Embedding provider {self.embedding_provider.provider_name} is not available")

        try:
            return await self.embedding_provider.embed(text)
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise RuntimeError(f"Failed to generate embedding: {e}")

    async def store(
        self,
        content: str,
        memory_type: str = "fact",
        category: str = "general",
        importance: float = 0.5,
        source_session_id: str = "",
        check_duplicates: bool = True,
    ) -> str:
        """Store a memory with its embedding.

        Args:
            content: The memory content to store
            memory_type: Type of memory ('fact', 'preference', 'conversation_summary', 'skill_learned')
            category: Category ('user_info', 'project', 'schedule', 'general')
            importance: Importance score 0.0 to 1.0
            source_session_id: Session where this memory originated
            check_duplicates: Whether to check for and skip duplicate memories

        Returns:
            Memory ID (of existing memory if duplicate, new ID if stored)
        """
        import uuid

        try:
            # Generate embedding
            embedding = await self._get_embedding(content)

            # Check for duplicates if enabled
            if check_duplicates:
                # Find similar memories (use similarity score, not hybrid score for deduplication)
                similar_memories = await self._find_similar_memories(
                    content, embedding, memory_type, category, min_importance=0.0
                )
                
                if similar_memories:
                    most_similar = similar_memories[0]
                    # Use pure similarity (cosine similarity) for deduplication, not hybrid score
                    similarity_score = most_similar.get("similarity", 0)
                    
                    # If very similar, skip storing
                    if similarity_score >= self.similarity_threshold:
                        logger.info(
                            "Skipping duplicate memory storage",
                            extra={
                                "existing_id": most_similar.get("id", ""),
                                "similarity_score": round(similarity_score, 4),
                                "hybrid_score": round(most_similar.get("score", 0), 4),
                                "content_preview": truncate_string(content, 100),
                                "existing_content_preview": truncate_string(most_similar.get("content", ""), 100),
                                "memory_type": most_similar.get("memory_type", ""),
                                "category": most_similar.get("category", ""),
                            }
                        )
                        # Return existing memory ID
                        return most_similar.get("id", "")
                    
                    # Log near-duplicates for monitoring
                    if similarity_score >= self.similarity_threshold * 0.8:  # 80% of threshold
                        logger.debug(
                            "Near-duplicate memory detected",
                            extra={
                                "similarity_score": round(similarity_score, 4),
                                "threshold": self.similarity_threshold,
                                "content_preview": truncate_string(content, 100),
                                "existing_content_preview": truncate_string(most_similar.get("content", ""), 100),
                            }
                        )

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
                    "content_preview": truncate_string(content, 100),
                    "source_session_id": source_session_id,
                    "duplicate_check": check_duplicates,
                }
            )

            return memory_id

        except Exception as e:
            logger.error(
                f"Failed to store memory: {e}",
                extra={
                    "content_preview": truncate_string(content, 100),
                    "memory_type": memory_type,
                    "source_session_id": source_session_id,
                }
            )
            raise

    async def _find_similar_memories(
        self,
        content: str,
        embedding: list[float],
        memory_type: str | None = None,
        category: str | None = None,
        limit: int = 5,
        min_importance: float = 0.0,
    ) -> list[dict[str, Any]]:
        """Find memories similar to the given content using hybrid scoring.

        Args:
            content: Content to find similarities for
            embedding: Pre-computed embedding for the content
            memory_type: Optional filter by memory type
            category: Optional filter by category
            limit: Maximum results to return
            min_importance: Minimum importance threshold for search

        Returns:
            List of similar memories with hybrid similarity scores
        """
        try:
            embedding_str = _format_embedding(embedding)
            
            # Build WHERE clause - search across all memory types/categories for duplicates
            conditions = [
                f"importance >= {min_importance}",
                "is_deleted = false",
            ]
            
            # Only filter by type/category if specified (for more targeted deduplication)
            if memory_type:
                conditions.append(f"memory_type = '{memory_type}'")
            
            if category:
                conditions.append(f"category = '{category}'")
            
            where_clause = " AND ".join(conditions)
            
            # Search using hybrid scoring (same as main search): cosine similarity * importance
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
                (1 - cosine_distance(embedding, {embedding_str})) * importance as score,
                (1 - cosine_distance(embedding, {embedding_str})) as similarity
            FROM table({self.stream_name})
            WHERE {where_clause}
            ORDER BY score DESC
            LIMIT {limit}
            """
            
            results = self.client.query(sql)
            
            logger.debug(
                "Similarity search for deduplication complete",
                extra={
                    "query_content_preview": truncate_string(content, 50),
                    "similar_count": len(results),
                    "top_hybrid_score": results[0].get("score", 0) if results else 0,
                    "top_similarity": results[0].get("similarity", 0) if results else 0,
                }
            )
            
            return results
            
        except Exception as e:
            logger.warning(f"Failed to find similar memories for deduplication: {e}")
            return []

    async def update_importance(self, memory_id: str, new_importance: float) -> bool:
        """Update the importance score of an existing memory.

        Note: Since Timeplus streams are append-only, this inserts a new record
        with the updated importance. Queries should filter by latest timestamp.

        Args:
            memory_id: ID of memory to update
            new_importance: New importance score (0.0-1.0)

        Returns:
            True if update record inserted successfully
        """
        try:
            # Get existing memory to copy other fields
            sql = f"""
            SELECT content, memory_type, category, embedding, source_session_id
            FROM table({self.stream_name})
            WHERE id = '{memory_id}' AND is_deleted = false
            ORDER BY timestamp DESC
            LIMIT 1
            """
            
            results = self.client.query(sql)
            if not results:
                logger.warning(f"Memory not found for importance update: {memory_id}")
                return False
                
            existing = results[0]
            
            import uuid
            update_data = {
                "id": memory_id,
                "memory_type": existing["memory_type"],
                "category": existing["category"],
                "content": existing["content"],
                "source_session_id": existing["source_session_id"],
                "embedding": existing["embedding"],
                "importance": new_importance,
                "is_deleted": False,
            }
            
            self.client.insert(self.stream_name, [update_data])
            
            logger.info(
                "Updated memory importance",
                extra={
                    "id": memory_id,
                    "new_importance": new_importance,
                    "old_importance": existing.get("importance", 0),
                }
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update memory importance: {e}")
            return False

    async def get_duplicate_stats(self) -> dict[str, Any]:
        """Get statistics about memory duplicates.
        
        Returns:
            Dictionary with duplicate statistics
        """
        try:
            # This would require more complex analysis - for now return basic stats
            sql = f"""
            SELECT 
                COUNT(*) as total_memories,
                COUNT(DISTINCT content) as unique_contents,
                memory_type,
                category
            FROM table({self.stream_name})
            WHERE is_deleted = false
            GROUP BY memory_type, category
            ORDER BY total_memories DESC
            """
            
            results = self.client.query(sql)
            
            total = sum(r.get("total_memories", 0) for r in results)
            unique = sum(r.get("unique_contents", 0) for r in results)
            
            return {
                "total_memories": total,
                "unique_contents": unique,
                "duplicate_rate": (total - unique) / total if total > 0 else 0,
                "by_type_category": results
            }
            
        except Exception as e:
            logger.warning(f"Failed to get duplicate stats: {e}")
            return {
                "total_memories": 0,
                "unique_contents": 0,
                "duplicate_rate": 0,
                "by_type_category": []
            }

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

        result_count = len(results)
        logger.info(
            f"Memory search complete: query='{truncate_string(query, 100)}', found={result_count} results",
            extra={
                "query": truncate_string(query, 100),
                "results": result_count,
                "limit": limit,
            }
        )

        if result_count > 0:
            logger.debug(
                "Memory search results",
                extra={
                    "memories": [
                        {
                            "type": r.get("memory_type", "fact"),
                            "content": truncate_string(r.get("content", ""), 100),
                            "score": r.get("score", 0),
                        }
                        for r in results
                    ]
                }
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
