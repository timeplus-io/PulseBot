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
        self.tool_logger = StreamWriter(batch_client, "tool_logs")

        self._running = False

        logger.info(f"Initialized agent: {agent_id}")

    async def run(self) -> None:
        """Main event loop - listen for messages targeting this agent."""
        self._running = True

        # Ensure all required streams exist before starting
        await self._ensure_streams_exist()

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

    async def _ensure_streams_exist(self) -> None:
        """Ensure all required Timeplus streams exist.

        Creates streams if they don't exist using CREATE STREAM IF NOT EXISTS.
        Note: Memory stream is optional and created separately when needed.
        """
        from pulsebot.timeplus.setup import (
            MESSAGES_STREAM_DDL,
            LLM_LOGS_STREAM_DDL,
            TOOL_LOGS_STREAM_DDL,
            EVENTS_STREAM_DDL,
        )

        logger.info("Ensuring required streams exist...")

        # Core streams required for agent operation
        streams = [
            ("messages", MESSAGES_STREAM_DDL),
            ("llm_logs", LLM_LOGS_STREAM_DDL),
            ("tool_logs", TOOL_LOGS_STREAM_DDL),
            ("events", EVENTS_STREAM_DDL),
        ]

        for name, ddl in streams:
            try:
                self.tp.execute(ddl)
                logger.debug(f"Ensured stream exists: {name}")
            except Exception as e:
                logger.warning(f"Could not create stream {name}: {e}")

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

            # Debug LLM response
            logger.debug(
                "LLM response details",
                extra={
                    "session_id": session_id,
                    "content_length": len(response.content) if response.content else 0,
                    "content_preview": truncate_string(response.content or "", 200) if response.content else "None",
                    "has_tool_calls": bool(response.tool_calls),
                    "tool_call_count": len(response.tool_calls or []),
                }
            )

            # Check if LLM wants to call tools
            if response.tool_calls:
                # Execute tools
                for tool_call in response.tool_calls:
                    # Broadcast tool call start to UI/CLI
                    await self._broadcast_tool_call(
                        session_id=session_id,
                        source=message.get("source", "webchat"),
                        tool_name=tool_call.name,
                        arguments=tool_call.arguments,
                        status="started",
                    )

                    # Execute and time the tool
                    import time
                    tool_start = time.time()
                    result = await self.executor.execute(
                        tool_name=tool_call.name,
                        arguments=tool_call.arguments,
                        session_id=session_id,
                    )
                    tool_duration_ms = int((time.time() - tool_start) * 1000)

                    # Extract result info (executor returns dict with success, output, error)
                    tool_success = result.get("success", False)
                    tool_output = result.get("output", "")
                    tool_error = result.get("error", "")
                    result_str = str(tool_output) if tool_success else f"Error: {tool_error}"

                    # Broadcast tool result to UI/CLI
                    await self._broadcast_tool_call(
                        session_id=session_id,
                        source=message.get("source", "webchat"),
                        tool_name=tool_call.name,
                        arguments=tool_call.arguments,
                        status="success" if tool_success else "error",
                        result=result_str,
                        duration_ms=tool_duration_ms,
                    )

                    # Log to tool_logs stream
                    await self._log_tool_call(
                        session_id=session_id,
                        tool_name=tool_call.name,
                        arguments=tool_call.arguments,
                        result=result_str,
                        status="success" if tool_success else "error",
                        duration_ms=tool_duration_ms,
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
                    context.add_tool_result(tool_call.id, result_str)
            else:
                # No tool calls - send final response
                response_content = response.content if response else ""
                if not response_content:
                    logger.warning(
                        "LLM returned empty response content",
                        extra={
                            "session_id": session_id,
                            "response_object": str(response)[:200] if response else "None"
                        }
                    )
                    response_content = "I'm not sure how to respond to that."

                await self._send_response(
                    session_id=session_id,
                    source_message=message,
                    response_text=response_content,
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
            final_text = response.content if response and response.content else ""
            if not final_text:
                final_text = (
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
        # Safely handle response which might be None in error cases
        response_content = response.content if response else ""
        response_usage = response.usage if response else None
        response_tool_calls = response.tool_calls if response else None
        
        await self.llm_logger.write({
            "session_id": session_id,
            "model": self.llm.model,
            "provider": self.llm.provider_name,
            "input_tokens": response_usage.input_tokens if response_usage else 0,
            "output_tokens": response_usage.output_tokens if response_usage else 0,
            "total_tokens": response_usage.total_tokens if response_usage else 0,
            "estimated_cost_usd": self.llm.estimate_cost(response_usage) if response_usage else 0.0,
            "latency_ms": int(latency_ms),
            "system_prompt_hash": hash_content(context.system_prompt),
            "system_prompt_preview": truncate_string(context.system_prompt, 200),
            "user_message_preview": truncate_string(
                context.messages[-1].get("content", "") if context.messages else "",
                200
            ),
            "assistant_response_preview": truncate_string(response_content or "", 200),
            "full_response_content": response_content or "",  # Full response for debugging
            "messages_count": len(context.messages),
            "tools_called": [tc.name for tc in (response_tool_calls or [])],
            "tool_call_count": len(response_tool_calls or []),
            "status": "success",
        })

    async def _broadcast_tool_call(
        self,
        session_id: str,
        source: str,
        tool_name: str,
        arguments: dict[str, Any],
        status: str,
        result: str | None = None,
        duration_ms: int = 0,
    ) -> None:
        """Broadcast tool call event to UI/CLI via messages stream.

        Args:
            session_id: Session identifier
            source: Original message source (for routing response)
            tool_name: Name of the tool being called
            arguments: Tool arguments
            status: 'started', 'success', or 'error'
            result: Tool result (for completed calls)
            duration_ms: Execution duration in milliseconds
        """
        # Create a readable summary of the tool call
        args_summary = self._format_tool_args(tool_name, arguments)

        content = {
            "tool_name": tool_name,
            "arguments": arguments,
            "args_summary": args_summary,
            "status": status,
        }
        if result is not None:
            content["result_preview"] = truncate_string(result, 200)
            content["duration_ms"] = duration_ms

        await self.messages_writer.write({
            "source": "agent",
            "target": f"channel:{source}",
            "session_id": session_id,
            "message_type": "tool_call",
            "content": json.dumps(content),
            "priority": 0,
        })

        logger.debug(
            f"Tool call broadcast: {tool_name} ({status})",
            extra={"session_id": session_id, "tool": tool_name},
        )

    def _format_tool_args(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """Format tool arguments into a readable summary.

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments dict

        Returns:
            Human-readable summary of what the tool is doing
        """
        # Common tool argument patterns
        if "command" in arguments:
            cmd = arguments["command"]
            return f"`{truncate_string(cmd, 80)}`"
        elif "query" in arguments:
            query = arguments["query"]
            return f'"{truncate_string(query, 60)}"'
        elif "path" in arguments:
            return f"`{arguments['path']}`"
        elif "url" in arguments:
            return f"`{arguments['url']}`"
        elif "filename" in arguments or "file" in arguments:
            filename = arguments.get("filename") or arguments.get("file")
            return f"`{filename}`"
        elif "content" in arguments:
            content = arguments["content"]
            return f'"{truncate_string(content, 40)}"'
        elif arguments:
            # Show first argument value
            first_key = next(iter(arguments))
            first_val = str(arguments[first_key])
            return f"{first_key}: {truncate_string(first_val, 50)}"
        return ""

    async def _log_tool_call(
        self,
        session_id: str,
        tool_name: str,
        arguments: dict[str, Any],
        result: str,
        status: str,
        duration_ms: int,
    ) -> None:
        """Log tool call to tool_logs stream.

        Args:
            session_id: Session identifier
            tool_name: Name of the tool
            arguments: Tool arguments
            result: Tool result string
            status: 'success' or 'error'
            duration_ms: Execution duration in milliseconds
        """
        await self.tool_logger.write({
            "session_id": session_id,
            "llm_request_id": "",
            "tool_name": tool_name,
            "skill_name": tool_name.split("_")[0] if "_" in tool_name else tool_name,
            "arguments": json.dumps(arguments),
            "status": status,
            "result_preview": truncate_string(result, 500),
            "error_message": result if status == "error" else "",
            "duration_ms": duration_ms,
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
            logger.info("Memory manager not available - skipping extraction")
            return

        if not self.memory.is_available():
            logger.info("Memory features not available - skipping extraction")
            return

        # Get last few messages for extraction
        recent_messages = context.messages[-5:] if len(context.messages) > 5 else context.messages
        message_count = len(recent_messages)

        logger.info(
            "Memory extraction started",
            extra={"session_id": session_id, "message_count": message_count}
        )

        extraction_prompt = build_memory_extraction_prompt()

        # Log the conversation being analyzed
        conversation_text = json.dumps(recent_messages, indent=2)
        logger.debug(
            f"Analyzing conversation for memory extraction",
            extra={
                "session_id": session_id,
                "conversation_preview": truncate_string(conversation_text, 500),
                "message_count": message_count,
                "conversation_lines": len(conversation_text.split('\n')) if conversation_text else 0
            }
        )

        try:
            extraction = await self.llm.chat(
                messages=[{
                    "role": "user",
                    "content": extraction_prompt + "\n\nConversation:\n" + conversation_text,
                }],
                system="You are a memory extraction assistant. Be concise. Return only valid JSON.",
            )

            logger.debug(
                f"Memory extraction LLM response",
                extra={
                    "session_id": session_id,
                    "response_length": len(extraction.content),
                    "response_preview": truncate_string(extraction.content, 200)
                }
            )

            # Handle various response formats the LLM might return
            response_content = extraction.content.strip()
            
            # Handle empty responses
            if not response_content:
                logger.info("Memory extraction returned empty response - no memories to store")
                return
            
            # Remove markdown code blocks if present
            if response_content.startswith("```"):
                # Find the end of the code block
                lines = response_content.split('\n')
                if lines[0].startswith("```"):
                    # Skip first line and find closing ```
                    content_lines = []
                    for line in lines[1:]:
                        if line.strip() == "```":
                            break
                        content_lines.append(line)
                    response_content = '\n'.join(content_lines).strip()
            
            # Handle case where response is just "[]" (empty array)
            if response_content == "[]":
                logger.info("Memory extraction returned empty array - no memories to store")
                return
            
            # Try to parse JSON
            try:
                memories = json.loads(response_content)
            except json.JSONDecodeError as e:
                logger.warning(f"Memory extraction JSON parse failed: {e}")
                logger.debug(
                    f"Invalid JSON content",
                    extra={
                        "session_id": session_id,
                        "content": truncate_string(response_content, 500)
                    }
                )
                
                # Try to extract JSON from within text (LLM sometimes adds explanatory text)
                import re
                json_match = re.search(r'\[[^\]]*\]', response_content)
                if json_match:
                    try:
                        memories = json.loads(json_match.group(0))
                        logger.info(f"Successfully extracted JSON from within text response")
                    except json.JSONDecodeError:
                        logger.warning("Could not extract valid JSON from text response")
                        return
                else:
                    # If no JSON found, try to see if it's a single object
                    obj_match = re.search(r'\{[^}]*\}', response_content)
                    if obj_match:
                        try:
                            obj = json.loads(obj_match.group(0))
                            memories = [obj] if isinstance(obj, dict) else []
                            logger.info(f"Successfully extracted single JSON object response")
                        except json.JSONDecodeError:
                            logger.warning("Could not extract valid JSON object from text response")
                            return
                    else:
                        return

            memory_count = len(memories) if isinstance(memories, list) else 0

            if memory_count == 0:
                logger.info("No memories extracted from conversation")
                return

            logger.info(f"Extracted {memory_count} memories from conversation")

            stored_count = 0
            for mem in memories:
                if isinstance(mem, dict) and "content" in mem:
                    mem_type = mem.get("type", "fact")
                    importance = mem.get("importance", 0.5)
                    content = mem["content"]

                    logger.info(
                        "Storing memory",
                        extra={
                            "type": mem_type,
                            "importance": importance,
                            "content_preview": truncate_string(content, 100),
                            "session_id": session_id,
                        }
                    )

                    await self.memory.store(
                        content=content,
                        memory_type=mem_type,
                        importance=importance,
                        source_session_id=session_id,
                    )
                    stored_count += 1

            logger.info(
                f"Memory extraction complete - stored {stored_count}/{memory_count} memories",
                extra={"session_id": session_id}
            )

        except Exception as e:
            logger.error(f"Memory extraction failed: {e}", exc_info=True)

    async def _log_error(self, message: dict[str, Any], error: Exception) -> None:
        """Log an error and send error response to client.

        Args:
            message: Message that caused the error
            error: The exception
        """
        session_id = message.get("session_id", "unknown")
        source = message.get("source", "webchat")
        error_msg = str(error)

        # Log error internally
        await self.messages_writer.write({
            "source": "agent",
            "target": "agent",
            "session_id": session_id,
            "message_type": "error",
            "content": json.dumps({
                "error": error_msg,
                "original_message_id": message.get("id"),
            }),
            "priority": 2,
        })

        # Send error response to client
        await self.messages_writer.write({
            "source": "agent",
            "target": f"channel:{source}",
            "session_id": session_id,
            "message_type": "agent_response",
            "content": json.dumps({
                "text": f"Sorry, an error occurred while processing your request: {error_msg}"
            }),
            "user_id": message.get("user_id", ""),
            "priority": 0,
        })
