"""System prompt templates for PulseBot."""

from datetime import datetime, timezone
from typing import Any


SYSTEM_PROMPT_TEMPLATE = """
You are {agent_name}, a helpful AI assistant powered by PulseBot.

## Core Identity
{custom_identity}

## Current Context
- Current time: {current_time}
- User: {user_name}
- Session: {session_id}
- Current time: {current_time}
- User: {user_name}
- Session: {session_id}
- Channel: {channel_name}
{model_info_section}

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
""".strip()


def build_system_prompt(
    agent_name: str,
    tools: list[Any],
    memories: list[dict[str, Any]] | None = None,
    user_name: str = "User",
    session_id: str = "",
    channel_name: str = "webchat",
    custom_identity: str = "I am a helpful, friendly AI assistant.",
    custom_instructions: str = "",
    model_info: str = "",
) -> str:
    """Build the complete system prompt.
    
    Args:
        agent_name: Name of the agent
        tools: List of ToolDefinition objects
        memories: List of relevant memory dicts
        user_name: User's display name
        session_id: Current session ID
        channel_name: Name of the channel (telegram, webchat, etc.)
        custom_identity: Custom identity/persona description
        custom_instructions: Additional custom instructions
        
    Returns:
        Formatted system prompt
    """
    # Format tools list
    if tools:
        tools_list = "\n".join([
            f"- **{t.name}**: {t.description}"
            for t in tools
        ])
    else:
        tools_list = "No tools are currently available."
    
    # Format memories
    if memories:
        memories_text = "\n".join([
            f"- [{m.get('memory_type', 'fact')}] {m.get('content', '')}"
            for m in memories
        ])
    else:
        memories_text = "No relevant memories found."
    
    return SYSTEM_PROMPT_TEMPLATE.format(
        agent_name=agent_name,
        custom_identity=custom_identity,
        current_time=datetime.now(timezone.utc).isoformat(),
        user_name=user_name,
        session_id=session_id[:8] if session_id else "new",
        channel_name=channel_name,
        tools_list=tools_list,
        memories=memories_text,
        custom_instructions=custom_instructions,
        model_info_section=f"\n## Model Configuration\n{model_info}" if model_info else "",
    )


def build_memory_extraction_prompt() -> str:
    """Get the prompt for extracting memories from conversations.
    
    Returns:
        Memory extraction prompt
    """
    return """
Review this conversation and extract any important facts, preferences, 
or information worth remembering about the user. 

CRITICAL: Return ONLY a valid JSON array in this exact format:
[{"type": "fact|preference|reminder", "content": "...", "importance": 0.0-1.0}]

If nothing is worth remembering, return an empty array: []

Examples of good extractions:
- [{"type": "fact", "content": "User's name is John Smith", "importance": 0.9}]
- [{"type": "preference", "content": "User prefers Python over Java", "importance": 0.7}]
- [{"type": "fact", "content": "User works at Acme Corp as Data Scientist", "importance": 0.8}]
- []

Be selective - only extract genuinely useful information like:
- User personal information (name, contact details, role, company)
- User preferences (communication style, interests, settings, favorite tools)
- Important facts (projects they're working on, technical expertise)
- Scheduled reminders or commitments
- Learned information that could help future interactions

Do NOT extract:
- Generic pleasantries or greetings
- Transient information
- Information already known/obvious
- Questions the user asked (unless they reveal preferences)

IMPORTANT: Respond with ONLY the JSON array. No other text, no explanations, no markdown formatting.
""".strip()
