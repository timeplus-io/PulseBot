# PulseBot Skills System

## Overview

PulseBot's skills system provides two ways to extend the agent's capabilities:

1. **Built-in Skills** - Python classes that register tools directly with the LLM (web search, file ops, shell)
2. **External Skills (agentskills.io)** - Markdown-based skill packages discovered from the filesystem, following the [agentskills.io](https://agentskills.io) open standard

Both types coexist seamlessly. Built-in skills expose tools the LLM can call directly. External skills use a **metadata-first loading pattern** where only name + description enter the system prompt at startup (~24 tokens per skill), and full instructions are loaded on demand via the `load_skill` tool.

## Architecture

```
pulsebot/skills/
├── base.py                  # BaseSkill, ToolDefinition, ToolResult
├── loader.py                # SkillLoader (built-in + external discovery)
├── __init__.py
├── agentskills/             # agentskills.io integration
│   ├── __init__.py
│   ├── models.py            # SkillMetadata, SkillContent
│   └── loader.py            # SKILL.md parser, validator, directory scanner
└── builtin/                 # Built-in skill implementations
    ├── __init__.py
    ├── web_search.py
    ├── file_ops.py
    ├── shell.py
    └── agentskills_bridge.py  # Bridge: load_skill + read_skill_file tools

skills/                      # Default directory for external skill packages
└── timeplus-sql-guide/      # Example skill
    ├── SKILL.md
    └── references/
        └── syntax-cheatsheet.md
```

## How Skills Work

### Skill Loading Flow

```
Startup
  │
  ├─ Load built-in skills (Python classes → tools registered directly)
  │    web_search, file_ops, shell
  │
  ├─ Discover external skills (scan skill_dirs for SKILL.md files)
  │    Parse YAML frontmatter → SkillMetadata (name + description only)
  │
  └─ If external skills found:
       Register AgentSkillsBridge skill → load_skill + read_skill_file tools
       Inject skill index into system prompt
```

### Two-Tier Loading (External Skills)

| Tier | When | What | Cost |
|------|------|------|------|
| Tier 1 - Metadata | Startup | Name + description in system prompt | ~24 tokens/skill |
| Tier 2 - Full Content | On demand via `load_skill` | Full SKILL.md instructions, scripts, references | ~2,000-5,000 tokens |

This means 25 external skills add only ~630 tokens to the base prompt, instead of 50,000-125,000 tokens if all instructions were loaded upfront.

### Tool Execution Flow

```
User Message → Agent
                    ↓
            LLM with Tools
                    ↓
            Tool Call Request
                    ↓
            SkillLoader.get_skill_for_tool()
                    ↓
            Skill.execute()
                    ↓
            ToolResult → LLM → Final Response
```

## Configuration

### Full Config Reference

```yaml
skills:
  # Built-in Python skills to load
  builtin:
    - web_search
    - file_ops
    - shell

  # Custom Python skill classes (module paths)
  custom: []

  # Directories to scan for agentskills.io skill packages
  skill_dirs:
    - "./skills"
    - "/shared/team-skills"

  # Skill names to skip during discovery
  disabled_skills: []
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `builtin` | list[str] | `["web_search", "file_ops", "shell"]` | Built-in skill names to load |
| `custom` | list[str] | `[]` | Module paths to custom Python skill classes |
| `skill_dirs` | list[str] | `[]` | Directories to scan for agentskills.io packages |
| `disabled_skills` | list[str] | `[]` | Skill names to skip (by `name` field in SKILL.md) |

### Enabling/Disabling External Skills

| Action | Configuration |
|--------|---------------|
| Enable external skills | Add directories to `skill_dirs` |
| Disable all external skills | Set `skill_dirs: []` or omit it |
| Disable specific skills | Add names to `disabled_skills` |
| Add more skill sources | Add more paths to `skill_dirs` |

### Docker Deployment

When running with Docker, mount the skills directory into the container:

```yaml
# docker-compose.yaml
pulsebot-agent:
  volumes:
    - ./config.yaml:/app/config.yaml:ro
    - ./skills:/app/skills:ro
```

## Built-in Skills

### Web Search (`web_search`)

Searches the web using Brave Search API or SearXNG.

**Tool**: `web_search`
- **Parameters**: `query` (string), `count` (integer, 1-10)
- **Returns**: List of search results with title, URL, and description

**Configuration**: Set `search.provider` to `"brave"` or `"searxng"` in config.yaml.

### File Operations (`file_ops`)

Read, write, and list files with security guardrails.

**Tools**:
- `read_file` - Read file contents (parameter: `path`)
- `write_file` - Write content to file (parameters: `path`, `content`, `append`)
- `list_directory` - List directory contents (parameter: `path`)

**Security**: Path traversal prevention ensures operations stay within the configured base path.

### Shell Commands (`shell`)

Execute shell commands with safety controls.

**Tool**: `run_command`
- **Parameters**: `command` (string)
- **Returns**: Exit code, stdout, stderr

**Safety Features**: Blocked commands list (`rm`, `sudo`, etc.), dangerous pattern detection, timeout protection (30s default), output size limits.

## External Skills (agentskills.io)

### The agentskills.io Standard

The [agentskills.io](https://agentskills.io) standard is a filesystem-based format for packaging AI agent skills, adopted by Claude, GitHub Copilot, OpenAI Codex, Cursor, and others.

A skill is a directory containing a `SKILL.md` file with YAML frontmatter for metadata and Markdown body for instructions:

```
my-skill/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: supplementary docs
└── assets/           # Optional: templates, data files
```

### SKILL.md Format

```markdown
---
name: my-skill
description: What this skill does and when to use it.
license: Apache-2.0
metadata:
  author: your-name
  version: "1.0"
compatibility: Requires X to be configured
allowed-tools: tool1 tool2
---

# My Skill

Full instructions loaded on demand by the agent.

## When to use this skill
Use when the user asks about X.

## Procedures
Step-by-step instructions...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars, lowercase letters, digits, hyphens. Must match directory name. |
| `description` | Yes | 1-1024 chars. Describes capability and trigger conditions. |
| `license` | No | License identifier (e.g., Apache-2.0) |
| `compatibility` | No | Environment requirements |
| `metadata` | No | Arbitrary key-value pairs (author, version, etc.) |
| `allowed-tools` | No | Space-delimited pre-approved tool list |

### How External Skills Are Used

1. At startup, PulseBot scans `skill_dirs` for directories containing `SKILL.md`
2. Only name + description are parsed and injected into the system prompt as a skill index
3. When the LLM determines a skill is relevant, it calls `load_skill` with the skill name
4. The full SKILL.md body (instructions, procedures, examples) is returned to the LLM
5. The LLM can read individual files from the skill package via `read_skill_file`

### Bridge Tools

The `AgentSkillsBridge` skill provides two tools for the LLM to interact with external skills:

| Tool | Description |
|------|-------------|
| `load_skill` | Load full instructions for a skill by name. Parameters: `skill_name` (string) |
| `read_skill_file` | Read a file from a skill's `scripts/` or `references/` directory. Parameters: `skill_name` (string), `file_path` (string) |

These tools are only registered when external skills are discovered. If `skill_dirs` is empty, they don't appear.

### Creating an External Skill

1. Create a directory under your skills path:

```bash
mkdir -p skills/my-skill/references
```

2. Create `SKILL.md` with frontmatter and instructions:

```markdown
---
name: my-skill
description: Guide for doing X when the user asks about Y.
---

# My Skill

## When to use
Use this skill when...

## Instructions
1. Do this
2. Then that
```

3. Optionally add reference files or scripts:

```bash
echo "# Cheatsheet" > skills/my-skill/references/cheatsheet.md
```

4. Restart PulseBot - the skill is automatically discovered.

## Custom Python Skills

For capabilities that require code execution (API calls, database queries), create a Python skill class.

### Creating a Custom Skill

```python
from pulsebot.skills.base import BaseSkill, ToolDefinition, ToolResult

class MySkill(BaseSkill):
    name = "my_skill"
    description = "Does something useful"

    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    def get_tools(self) -> list[ToolDefinition]:
        return [ToolDefinition(
            name="my_tool",
            description="Clear description for the LLM",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to look up"
                    }
                },
                "required": ["query"]
            }
        )]

    async def execute(self, tool_name: str, arguments: dict) -> ToolResult:
        if tool_name == "my_tool":
            # Your implementation here
            return ToolResult.ok("Result data")
        return ToolResult.fail(f"Unknown tool: {tool_name}")
```

### Registering Custom Skills

Add to `config.yaml`:

```yaml
skills:
  custom:
    - my_project.skills.my_skill.MySkill
```

### Best Practices

- **Input Validation**: Always validate arguments before processing
- **Error Handling**: Return descriptive errors via `ToolResult.fail()`
- **Security**: Validate paths, commands, and external inputs
- **Timeouts**: Use `asyncio.wait_for()` for external API calls
- **Naming**: Use descriptive, action-oriented tool names (`get_weather`, not `weather`)
- **Descriptions**: Write clear descriptions - this is what the LLM uses to decide when to call your tool

## When to Use Which Approach

| Use Case | Approach |
|----------|----------|
| Need to call APIs, run code, access databases | Custom Python skill |
| Procedural knowledge, guides, SQL templates | External agentskills.io skill |
| Team-shared domain knowledge | External skill in a shared `skill_dirs` path |
| Portable across AI platforms | External skill (agentskills.io standard) |
| Core agent capability | Built-in skill |

## Troubleshooting

**External skill not discovered**:
- Verify the directory contains a `SKILL.md` file
- Check that `name` in frontmatter matches the directory name exactly
- Ensure the directory is inside a path listed in `skill_dirs`
- Check that the skill name is not in `disabled_skills`
- Look for validation warnings in logs

**`load_skill` / `read_skill_file` tools not available**:
- These only appear when at least one external skill is discovered
- Verify `skill_dirs` is configured and contains valid skill packages

**"Unknown built-in skill" error**:
- Check that the skill name matches one of: `web_search`, `file_ops`, `shell`

**"Failed to load custom skill" error**:
- Ensure the module path is importable (in Python path)
- Verify the class exists and inherits from `BaseSkill`
- Check for import errors in the skill module

**Tool not being called by LLM**:
- Check tool description is clear and specific
- Ensure parameter schema is correct JSON Schema
- Verify tool name is unique across all skills
