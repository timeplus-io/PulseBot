"""SQLAlchemy models for PostgreSQL metadata storage."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def new_uuid() -> uuid.UUID:
    """Generate new UUID."""
    return uuid.uuid4()


class Base(DeclarativeBase):
    """Base class for all models."""
    
    type_annotation_map = {
        dict[str, Any]: JSONB,
    }


class Agent(Base):
    """Agent configuration."""
    
    __tablename__ = "agents"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    model: Mapped[str] = mapped_column(String(255), nullable=False, default="claude-sonnet-4-20250514")
    provider: Mapped[str] = mapped_column(String(50), nullable=False, default="anthropic")
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    temperature: Mapped[float] = mapped_column(Float, default=0.7)
    max_tokens: Mapped[int] = mapped_column(Integer, default=4096)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
    
    # Relationships
    skills: Mapped[list["AgentSkill"]] = relationship(
        "AgentSkill", back_populates="agent", cascade="all, delete-orphan"
    )
    channels: Mapped[list["Channel"]] = relationship(
        "Channel", back_populates="agent", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Agent(name='{self.name}', model='{self.model}')>"


class Skill(Base):
    """Skills registry."""
    
    __tablename__ = "skills"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    module_path: Mapped[str] = mapped_column(String(500), nullable=False)
    config: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    
    # Relationships
    agents: Mapped[list["AgentSkill"]] = relationship(
        "AgentSkill", back_populates="skill", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Skill(name='{self.name}')>"


class AgentSkill(Base):
    """Agent-Skill mapping with optional config overrides."""
    
    __tablename__ = "agent_skills"
    
    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True
    )
    config_override: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    
    # Relationships
    agent: Mapped["Agent"] = relationship("Agent", back_populates="skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="agents")


class Channel(Base):
    """Channel configurations."""
    
    __tablename__ = "channels"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # 'telegram', 'slack', etc.
    config: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    agent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    
    # Relationships
    agent: Mapped["Agent | None"] = relationship("Agent", back_populates="channels")
    
    def __repr__(self) -> str:
        return f"<Channel(name='{self.name}', enabled={self.enabled})>"


class MCPServer(Base):
    """MCP Server registry."""
    
    __tablename__ = "mcp_servers"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    transport: Mapped[str] = mapped_column(String(50), default="stdio")  # 'stdio', 'http', 'ws'
    command: Mapped[str | None] = mapped_column(String(500), nullable=True)
    args: Mapped[list[str]] = mapped_column(JSONB, default=list)
    config: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    
    def __repr__(self) -> str:
        return f"<MCPServer(name='{self.name}', transport='{self.transport}')>"


class ScheduledTask(Base):
    """Scheduled tasks (mirrors Timeplus tasks for UI management)."""
    
    __tablename__ = "scheduled_tasks"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    schedule: Mapped[str] = mapped_column(String(100), nullable=False)  # Cron or interval
    task_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'heartbeat', 'summary', 'custom'
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_run: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    
    def __repr__(self) -> str:
        return f"<ScheduledTask(name='{self.name}', schedule='{self.schedule}')>"


class UserIdentity(Base):
    """User sessions for identity linking across channels."""
    
    __tablename__ = "user_identities"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    canonical_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Unified user ID
    channel: Mapped[str] = mapped_column(String(100), nullable=False)
    channel_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    user_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)  # Renamed from 'metadata' (reserved)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    
    __table_args__ = (
        # Unique constraint on channel + channel_user_id
        {"sqlite_autoincrement": True},
    )
    
    def __repr__(self) -> str:
        return f"<UserIdentity(canonical_id='{self.canonical_id}', channel='{self.channel}')>"
