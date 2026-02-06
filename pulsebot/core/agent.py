"""Main agent loop for PulseBot."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

from pulsebot.core.context import ContextBuilder
from pulsebot.core.executor import ToolExecutor
from pulsebot.core.prompts import build_memory_extraction_prompt
from pulsebot.timeplus.streams import StreamReader, StreamWriter
from pulsebot.utils import get_logger, hash_content, truncate_string

if TYPE_CHECKING:
    from pulsebot.config import Config, TimeplusConfig
    from pulsebot.providers.base import LLMProvider
    from pulsebot.skills.loader import SkillLoader
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.timeplus.memory import MemoryManager

logger = get_logger(__name__)


class Agent:
    """
    The main agent that:
    1. Listens to the messages stream for incoming requests
    2. Builds context from memory and conversation history
    3. Calls LLM for reasoning
    4. Executes tools and writes results back to stream
    
    Example:
        >>> agent = Agent(
        ...     agent_id="main",
        ...     timeplus=client,
        ...     llm_provider=anthropic_provider,
        ...     skill_loader=skills,
        ... )
        >>> await agent.run()
    """
    
    def __init__(
        self,
        agent_id: str,
        timeplus: "TimeplusClient",
        llm_provider: "LLMProvider",
        skill_loader: "SkillLoader",
        memory_manager: "MemoryManager | None" = None,
        agent_name: str = "PulseBot",
        model_info: str = "",
        max_iterations: int = 10,
        timeplus_config: "TimeplusConfig | None" = None,
    ):
        """Initialize the agent.

        Args:
            agent_id: Unique agent identifier
            timeplus: Timeplus client for streaming operations
            llm_provider: LLM provider for reasoning
            skill_loader: Loaded skills
            memory_manager: Optional memory manager
            agent_name: Display name
            max_iterations: Max tool call iterations per request
            timeplus_config: Timeplus config for creating additional clients
        """
        from pulsebot.timeplus.client import TimeplusClient

        self.agent_id = agent_id
        self.tp = timeplus
        self.llm = llm_provider
        self.skills = skill_loader
        self.memory = memory_manager
        self.agent_name = agent_name
        self.model_info = model_info
        self.max_iterations = max_iterations

        # Create a separate client for batch queries to avoid
        # "Simultaneous queries on single connection" error
        if timeplus_config:
            batch_client = TimeplusClient.from_config(timeplus_config)
        else:
            # Fallback: create new client with same connection params
            batch_client = TimeplusClient(
                host=timeplus.host,
                port=timeplus.port,
                username=timeplus.username,
                password=timeplus.password,
            )

        # Initialize components - use separate client for context builder
        self.context_builder = ContextBuilder(
            timeplus_client=batch_client,
            memory_manager=memory_manager,
            agent_name=agent_name,
            model_info=model_info,
        )
        self.executor = ToolExecutor(skill_loader)

        # Stream reader uses main client for streaming query
        self.messages_reader = StreamReader(timeplus, "messages")
        # Writers use batch client to avoid conflicts with streaming query
        self.messages_writer = StreamWriter(batch_client, "messages")
        self.llm_logger = StreamWriter(batch_client, "llm_logs")
        
        self._running = False
        
        logger.info(f"Initialized agent: {agent_id}")
    
    async def run(self) -> None:
        """Main event loop - listen for messages targeting this agent."""
        self._running = True
        
        query = """
            SELECT * FROM messages 
            WHERE target = 'agent' 
              AND message_type IN ('user_input', 'tool_result', 'heartbeat', 'scheduled_task')
            SETTINGS seek_to='latest'
        """
        
        logger.info(f"Agent {self.agent_id} starting message loop")
        
        try:
            async for message in self.messages_reader.stream(query):
                if not self._running:
                    break
                
                try:
                    await self._process_message(message)
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    await self._log_error(message, e)
        finally:
            self._running = False
            logger.info(f"Agent {self.agent_id} stopped")
    
    async def stop(self) -> None:
        """Stop the agent loop."""
        self._running = False
    
    async def _process_message(self, message: dict[str, Any]) -> None:
        """Process a single incoming message through the agent loop.
        
        Args:
            message: Raw message from stream
        """
        session_id = message.get("session_id", "")
        message_type = message.get("message_type", "")
        content_str = message.get("content", "{}")
        
        try:
            content = json.loads(content_str)
        except json.JSONDecodeError:
            content = {"text": content_str}
        
        user_message = content.get("text", "")
        
        logger.info(
            "Processing message",
            extra={
                "session_id": session_id,
                "type": message_type,
                "preview": truncate_string(user_message, 50),
            }
        )
        
        # Build context from memory + recent conversation
        context = await self.context_builder.build(
            session_id=session_id,
            user_message=user_message,
            tools=self.skills.get_tools(),
            include_memory=True,
            memory_limit=10,
        )
        
        # Get tool definitions
        tools = self.executor.get_tool_definitions()
        
        # Agent loop: keep calling LLM until no more tool calls
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # Call LLM
            import time
            start_time = time.time()
            
            response = await self.llm.chat(
                messages=context.messages,
                tools=tools if tools else None,
                system=context.system_prompt,
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Log to observability stream
            await self._log_llm_call(session_id, context, response, latency_ms)
            
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
                    context.add_assistant_message(
                        content=response.content or "",
                        tool_calls=[{
                            "id": tool_call.id,
                            "function": {
                                "name": tool_call.name,
                                "arguments": json.dumps(tool_call.arguments),
                            },
                        }],
                    )
                    context.add_tool_result(tool_call.id, result)
            else:
                # No tool calls - send final response
                await self._send_response(
                    session_id=session_id,
                    source_message=message,
                    response_text=response.content,
                )

                # Extract and store any new memories
                if self.memory:
                    await self._extract_memories(session_id, context, response)

                break
        else:
            # Max iterations reached - send partial response or error
            logger.warning(
                f"Max iterations ({self.max_iterations}) reached",
                extra={"session_id": session_id}
            )
            final_text = response.content if response and response.content else (
                "I apologize, but I wasn't able to complete this task within the allowed "
                "number of steps. Please try breaking down your request into smaller parts."
            )
            await self._send_response(
                session_id=session_id,
                source_message=message,
                response_text=final_text,
            )

    async def _send_response(
        self,
        session_id: str,
        source_message: dict[str, Any],
        response_text: str,
    ) -> None:
        """Write agent response back to the messages stream.
        
        Args:
            session_id: Session identifier
            source_message: Original message we're responding to
            response_text: Response content
        """
        source = source_message.get("source", "webchat")
        
        await self.messages_writer.write({
            "source": "agent",
            "target": f"channel:{source}",
            "session_id": session_id,
            "message_type": "agent_response",
            "content": json.dumps({"text": response_text}),
            "user_id": source_message.get("user_id", ""),
            "channel_metadata": source_message.get("channel_metadata", ""),
            "priority": 0,
        })
        
        logger.info(
            "Sent response",
            extra={
                "session_id": session_id,
                "target": f"channel:{source}",
                "length": len(response_text),
            }
        )
    
    async def _log_llm_call(
        self,
        session_id: str,
        context: Any,
        response: Any,
        latency_ms: float,
    ) -> None:
        """Log LLM call to observability stream.
        
        Args:
            session_id: Session identifier
            context: Context used for the call
            response: LLM response
            latency_ms: Request latency in milliseconds
        """
        await self.llm_logger.write({
            "session_id": session_id,
            "model": self.llm.model,
            "provider": self.llm.provider_name,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
            "estimated_cost_usd": self.llm.estimate_cost(response.usage),
            "latency_ms": int(latency_ms),
            "system_prompt_hash": hash_content(context.system_prompt),
            "user_message_preview": truncate_string(
                context.messages[-1].get("content", "") if context.messages else "", 
                200
            ),
            "assistant_response_preview": truncate_string(response.content or "", 200),
            "tools_called": [tc.name for tc in (response.tool_calls or [])],
            "tool_call_count": len(response.tool_calls or []),
            "status": "success",
        })
    
    async def _extract_memories(
        self,
        session_id: str,
        context: Any,
        response: Any,
    ) -> None:
        """Extract important information to store as memories.
        
        Args:
            session_id: Session identifier
            context: Conversation context
            response: Final LLM response
        """
        if not self.memory:
            return
        
        # Get last few messages for extraction
        recent_messages = context.messages[-5:] if len(context.messages) > 5 else context.messages
        
        extraction_prompt = build_memory_extraction_prompt()
        
        try:
            extraction = await self.llm.chat(
                messages=[{
                    "role": "user",
                    "content": extraction_prompt + "\n\nConversation:\n" + json.dumps(recent_messages),
                }],
                system="You are a memory extraction assistant. Be concise. Return only valid JSON.",
            )
            
            memories = json.loads(extraction.content)
            
            for mem in memories:
                if isinstance(mem, dict) and "content" in mem:
                    await self.memory.store(
                        content=mem["content"],
                        memory_type=mem.get("type", "fact"),
                        importance=mem.get("importance", 0.5),
                        source_session_id=session_id,
                    )
                    
                    logger.debug(
                        "Stored memory",
                        extra={"content": truncate_string(mem["content"], 50)},
                    )
                    
        except (json.JSONDecodeError, Exception) as e:
            logger.debug(f"No memories extracted: {e}")
    
    async def _log_error(self, message: dict[str, Any], error: Exception) -> None:
        """Log an error that occurred during processing.
        
        Args:
            message: Message that caused the error
            error: The exception
        """
        session_id = message.get("session_id", "unknown")
        
        await self.messages_writer.write({
            "source": "agent",
            "target": "agent",
            "session_id": session_id,
            "message_type": "error",
            "content": json.dumps({
                "error": str(error),
                "original_message_id": message.get("id"),
            }),
            "priority": 2,
        })


