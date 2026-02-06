"""Timeplus client wrapper for PulseBot."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, AsyncIterator

from proton_driver import client

from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.config import TimeplusConfig

logger = get_logger(__name__)


class TimeplusClient:
    """
    Wrapper around proton-python-driver for both batch and streaming queries.
    
    The client uses native protocol on port 8463 for all operations.
    
    Example:
        >>> client = TimeplusClient.from_config(config.timeplus)
        >>> result = client.query("SELECT * FROM table(messages) LIMIT 10")
        >>> async for row in client.stream_query("SELECT * FROM messages"):
        ...     print(row)
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8463,
        username: str = "default",
        password: str = "",
    ):
        """Initialize Timeplus client.
        
        Args:
            host: Timeplus server hostname
            port: Native protocol port (default 8463)
            username: Database username
            password: Database password
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        
        # Initialize client lazily
        self._client: client.Client | None = None
        
        logger.info(
            "Initialized Timeplus client",
            extra={"host": host, "port": port}
        )
    
    @classmethod
    def from_config(cls, config: TimeplusConfig) -> "TimeplusClient":
        """Create client from configuration object."""
        return cls(
            host=config.host,
            port=config.port,
            username=config.username,
            password=config.password,
        )
    
    @property
    def _get_client(self) -> client.Client:
        """Get or create client (lazy initialization)."""
        if self._client is None:
            self._client = client.Client(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
            )
        return self._client
    
    def execute(self, query: str) -> Any:
        """Execute a DDL or command query.
        
        Use for CREATE, DROP, ALTER, INSERT without SELECT, etc.
        
        Args:
            query: SQL command to execute
            
        Returns:
            Command result (usually None for DDL)
        """
        logger.debug("Executing command", extra={"query": query[:100]})
        return self._get_client.execute(query)
    
    def query(self, query: str) -> list[dict[str, Any]]:
        """Execute a historical query and return results as list of dicts.

        Use for SELECT queries on table() data.

        Args:
            query: SQL SELECT query

        Returns:
            List of row dictionaries
        """
        logger.debug("Executing query", extra={"query": query[:100]})

        # Use execute_iter with column types to get column names
        result_iter = self._get_client.execute_iter(query, with_column_types=True)

        # First item contains column metadata: [(name, type), ...]
        columns_with_types = next(result_iter)
        column_names = [col[0] for col in columns_with_types]

        # Convert rows to dictionaries
        rows = []
        for row in result_iter:
            rows.append(dict(zip(column_names, row)))

        return rows
    
    def insert(
        self,
        stream: str,
        data: list[dict[str, Any]],
        column_names: list[str] | None = None,
    ) -> None:
        """Insert data into a stream.
        
        Args:
            stream: Target stream name
            data: List of row dictionaries
            column_names: Optional explicit column order
        """
        if not data:
            return
        
        if column_names is None:
            column_names = list(data[0].keys())
        
        rows = [[row.get(col) for col in column_names] for row in data]
        
        logger.debug(
            "Inserting data",
            extra={"stream": stream, "rows": len(rows), "columns": column_names}
        )
        
        # Build INSERT query
        placeholders = ", ".join(column_names)
        query = f"INSERT INTO {stream} ({placeholders}) VALUES"
        
        self._get_client.execute(query, rows)
    
    async def stream_query(self, query: str) -> AsyncIterator[dict[str, Any]]:
        """Execute a streaming query and yield results as they arrive.
        
        Uses execute_iter() for unbounded streaming queries.
        
        Args:
            query: Streaming SQL query
            
        Yields:
            Row dictionaries as they arrive
        """
        logger.debug("Starting stream query", extra={"query": query[:100]})
        
        # Run the blocking stream in a thread pool
        def _stream_sync():
            # Use with_column_types=True to get column metadata
            result = self._get_client.execute_iter(
                query,
                with_column_types=True
            )
            
            # First item contains column metadata
            columns_with_types = next(result)
            column_names = [col[0] for col in columns_with_types]
            
            # Subsequent items are data rows (tuples)
            for row in result:
                # Convert tuple to dictionary
                yield dict(zip(column_names, row))
        
        # Use asyncio to yield from the sync generator
        loop = asyncio.get_event_loop()
        queue: asyncio.Queue[Any | None] = asyncio.Queue()
        
        async def producer():
            def run():
                try:
                    for row in _stream_sync():
                        asyncio.run_coroutine_threadsafe(
                            queue.put(row), loop
                        ).result()
                finally:
                    asyncio.run_coroutine_threadsafe(
                        queue.put(None), loop
                    ).result()
            
            await loop.run_in_executor(None, run)
        
        # Start producer task
        producer_task = asyncio.create_task(producer())
        
        try:
            while True:
                row = await queue.get()
                if row is None:
                    break
                yield row
        finally:
            producer_task.cancel()
    
    def ping(self) -> bool:
        """Check if Timeplus server is reachable.
        
        Returns:
            True if server responds, False otherwise
        """
        try:
            self.execute("SELECT 1")
            return True
        except Exception as e:
            logger.warning("Ping failed", extra={"error": str(e)})
            return False
    
    def close(self) -> None:
        """Close client connections."""
        if self._client is not None:
            try:
                self._client.disconnect()
            except Exception:
                pass
            self._client = None
        
        logger.info("Closed Timeplus connections")
