"""PostgreSQL connection management for PulseBot."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from pulsebot.db.models import Base
from pulsebot.utils import get_logger

if TYPE_CHECKING:
    from pulsebot.config import PostgresConfig

logger = get_logger(__name__)

# Global session factory
_session_factory: async_sessionmaker[AsyncSession] | None = None


class DatabaseManager:
    """PostgreSQL database manager.
    
    Handles connection pooling and session management using async SQLAlchemy.
    
    Example:
        >>> db = DatabaseManager.from_config(config.postgres)
        >>> await db.initialize()
        >>> async with db.session() as session:
        ...     agents = await session.execute(select(Agent))
    """
    
    def __init__(
        self,
        url: str,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        """Initialize database manager.
        
        Args:
            url: SQLAlchemy async database URL
            echo: Echo SQL statements for debugging
            pool_size: Connection pool size
            max_overflow: Max connections above pool size
        """
        self.url = url
        self.engine = create_async_engine(
            url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        logger.info("Initialized database manager")
    
    @classmethod
    def from_config(cls, config: "PostgresConfig", echo: bool = False) -> "DatabaseManager":
        """Create database manager from configuration.
        
        Args:
            config: PostgreSQL configuration
            echo: Echo SQL for debugging
        """
        return cls(url=config.url, echo=echo)
    
    async def initialize(self) -> None:
        """Create all tables if they don't exist."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables initialized")
    
    async def drop_all(self) -> None:
        """Drop all tables (use with caution!)."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        
        logger.warning("All database tables dropped")
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session context manager.
        
        Automatically handles commit/rollback and cleanup.
        
        Yields:
            Async database session
        """
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
    
    async def close(self) -> None:
        """Close database connections."""
        await self.engine.dispose()
        logger.info("Database connections closed")
    
    async def ping(self) -> bool:
        """Check database connectivity.
        
        Returns:
            True if database is reachable
        """
        try:
            async with self.session() as session:
                await session.execute("SELECT 1")
            return True
        except Exception as e:
            logger.warning(f"Database ping failed: {e}")
            return False


def init_session_factory(config: "PostgresConfig", echo: bool = False) -> None:
    """Initialize the global session factory.
    
    Call this during application startup.
    
    Args:
        config: PostgreSQL configuration
        echo: Echo SQL for debugging
    """
    global _session_factory
    
    engine = create_async_engine(
        config.url,
        echo=echo,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )
    _session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    logger.info("Initialized global session factory")


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session from the global factory.
    
    Use this in API routes and other code that needs database access.
    
    Yields:
        Async database session
        
    Raises:
        RuntimeError: If session factory not initialized
    """
    if _session_factory is None:
        raise RuntimeError("Database session factory not initialized. Call init_session_factory first.")
    
    session = _session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
