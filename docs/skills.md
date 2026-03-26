# PulseBot Skills System

## Overview

PulseBot's skills system provides three ways to extend the agent's capabilities:

1. **Built-in Skills** - Python classes that register tools directly with the LLM (web search, file ops, shell)
2. **External Skills (agentskills.io)** - Markdown-based skill packages discovered from the filesystem, following the [agentskills.io](https://agentskills.io) open standard
3. **OpenClaw Skills** - Enhanced agentskills.io packages with runtime requirements, ClawHub registry integration, and automatic dependency checking

All three types coexist seamlessly. Built-in skills expose tools the LLM can call directly. External skills use a **metadata-first loading pattern** where only name + description enter the system prompt at startup (~24 tokens per skill), and full instructions are loaded on demand via the `load_skill` tool.

## Architecture

```
pulsebot/skills/
├── base.py                 # BaseSkill, ToolDefinition, ToolResult
├── loader.py               # SkillLoader (built-in + external discovery)
├── lock.py                 # LockFile manager for ClawHub-installed skills
├── clawhub_client.py       # ClawHub registry REST API client
├── __init__.py
├── agentskills/            # agentskills.io integration
│   ├── __init__.py
│   ├── models.py           # SkillMetadata, SkillContent, OpenClawMetadata
│   ├── loader.py           # SKILL.md parser, validator, directory scanner
│   └── requirements.py     # Runtime requirement checker
└── builtin/                # Built-in skill implementations
    ├── __init__.py

    ├── file_ops.py
    ├── shell.py
    └── agentskills_bridge.py  # Bridge: load_skill + read_skill_file tools

skills/                     # Default directory for external skill packages
└── timeplus-sql-guide/     # Example skill
    ├── SKILL.md
    └── references/
        └── syntax-cheatsheet.md

.clawhub/                   # ClawHub registry metadata
└── lock.json               # Tracks installed skills with content hashes
```

## How Skills Work

### Skill Loading Flow

```
Startup
│
├─ Load built-in skills (Python classes → tools registered directly)
│   file_ops, shell
│
├─ Discover external skills (scan skill_dirs for SKILL.md files)
│   Parse YAML frontmatter → SkillMetadata (name + description only)
│   Check OpenClaw requirements → Skip if not satisfied
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

    - file_ops
    - shell
    - workspace

  # Directories to scan for agentskills.io skill packages
  skill_dirs:
    - "./skills"
    - "/shared/team-skills"

  # Skill names to skip during discovery
  disabled_skills: []

# ClawHub registry settings
clawhub:
  # Directory to install ClawHub skills (defaults to first skill_dirs entry)
  install_dir: "./skills"

  # Auto-update installed skills on startup
  auto_update: false

  # Auth token — supports env var substitution like other API keys (preferred)
  auth_token: "${CLAWHUB_AUTH_TOKEN:-}"

  # Alternative: read token from a file instead of config
  # auth_token_path: "~/.clawhub/token"
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `skills.builtin` | list[str] | `["file_ops", "shell", "workspace"]` | Built-in skill names to load |
| `skills.skill_dirs` | list[str] | `[]` | Directories to scan for agentskills.io packages |
| `skills.disabled_skills` | list[str] | `[]` | Skill names to skip (by `name` field in SKILL.md) |
| `clawhub.install_dir` | str | First `skill_dirs` entry | Default directory for `pulsebot skill install` |
| `clawhub.auto_update` | bool | `false` | Auto-update installed skills on startup |
| `clawhub.auth_token` | str | `""` | ClawHub auth token — supports `${CLAWHUB_AUTH_TOKEN:-}` env var substitution (preferred) |
| `clawhub.auth_token_path` | str | `None` | Alternative: path to file containing ClawHub auth token (used if `auth_token` is empty) |

### Enabling/Disabling External Skills

| Action | Configuration |
|--------|---------------|
| Enable external skills | Add directories to `skill_dirs` |
| Disable all external skills | Set `skill_dirs: []` or omit it |
| Disable specific skills | Add names to `disabled_skills` |
| Add more skill sources | Add more paths to `skill_dirs` |
| Auto-update ClawHub skills | Set `clawhub.auto_update: true` |

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

### Workspace (`workspace`)

Manages isolated workspace directories for sessions and tasks.

**Tools**:
- `create_workspace` - Create a new workspace
- `list_workspaces` - List available workspaces
- `get_workspace_files` - List files in a workspace
- `read_workspace_file` - Read a file from a workspace

## External Skills (agentskills.io)

### The agentskills.io Standard

The [agentskills.io](https://agentskills.io) standard is a filesystem-based format for packaging AI agent skills, adopted by Claude, GitHub Copilot, OpenAI Codex, Cursor, and others.

A skill is a directory containing a `SKILL.md` file with YAML frontmatter for metadata and Markdown body for instructions:

```
my-skill/
├── SKILL.md              # Required: metadata + instructions
├── scripts/              # Optional: executable code
├── references/           # Optional: supplementary docs
└── assets/               # Optional: templates, data files
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

## OpenClaw-Compatible Skills

OpenClaw extends the agentskills.io standard with runtime requirements and ClawHub registry integration. Skills can declare what they need (binaries, environment variables, OS) and PulseBot will only load them if requirements are satisfied.

### OpenClaw Metadata Block

Add an `openclaw` (or `clawdbot`, `clawdis`, `moltbot`) block to your SKILL.md frontmatter:

```markdown
---
name: my-advanced-skill
description: A skill that requires specific tools and environment.
metadata:
  openclaw:
    # Requirements that must ALL be satisfied
    requires:
      # Required environment variables
      env:
        - MY_API_KEY
        - DATABASE_URL
      
      # Required binaries (all must exist in PATH)
      bins:
        - docker
        - kubectl
      
      # At least ONE of these must exist
      anyBins:
        - jq
        - python3
      
      # Required config files
      configs:
        - ~/.myapp/config.yaml
    
    # Primary env var shown in error messages
    primaryEnv: MY_API_KEY
    
    # Bypass requirement checks (use with caution)
    always: false
    
    # Emoji for display
    emoji: 🔧
    
    # Supported operating systems
    os:
      - darwin
      - linux
    
    # ClawHub skill key for updates
    skillKey: my-team/my-advanced-skill
---
```

### OpenClaw Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `openclaw.requires.env` | list[str] | Required environment variables |
| `openclaw.requires.bins` | list[str] | Required binaries (all must exist) |
| `openclaw.requires.anyBins` | list[str] | Alternative binaries (at least one must exist) |
| `openclaw.requires.configs` | list[str] | Required configuration files |
| `openclaw.primaryEnv` | str | Primary env var to show in error messages |
| `openclaw.always` | bool | If true, bypass all requirement checks |
| `openclaw.emoji` | str | Emoji for display in skill listings |
| `openclaw.homepage` | str | URL to skill documentation |
| `openclaw.os` | list[str] | Supported OS: `darwin`, `linux`, `win32` |
| `openclaw.skillKey` | str | ClawHub registry key for auto-updates |

### Aliases for OpenClaw Block

The following top-level keys are all aliases for the OpenClaw metadata block:

- `openclaw` (preferred)
- `clawdbot`
- `clawdis`
- `moltbot`

Example with alias:

```markdown
---
name: my-skill
metadata:
  clawdbot:
    requires:
      env: [API_KEY]
      bins: [curl]
---
```

### How Requirement Checking Works

When PulseBot discovers an external skill:

1. Parse SKILL.md frontmatter
2. If `openclaw` metadata exists:
   - Check OS compatibility
   - Verify all required binaries exist in PATH
   - Check that at least one of `anyBins` exists
   - Verify all required environment variables are set
   - Check that required config files exist
3. If `always: true`, skip all checks
4. If any check fails, the skill is skipped with a warning logged
5. If no `openclaw` metadata, the skill loads normally (backward compatible)

Binary lookups are cached per startup for performance.

## ClawHub Registry

ClawHub is a public registry for OpenClaw-compatible skills. Install skills directly from the registry with automatic dependency checking.

### CLI Commands

```bash
# Search for skills in ClawHub
pulsebot skill search <query>

# Install a skill from ClawHub
pulsebot skill install <slug> [--version VERSION] [--dir DIR]

# List installed ClawHub skills
pulsebot skill list [--dir WORKDIR]

# Remove an installed skill
pulsebot skill remove <slug> [--dir DIR] [--workdir WORKDIR]
```

### Authentication

To install skills from ClawHub, you need to set the `CLAWHUB_AUTH_TOKEN` environment variable:

```bash
# Set the authentication token
export CLAWHUB_AUTH_TOKEN=your_token_here

# Or use a .env file
CLAWHUB_AUTH_TOKEN=your_token_here
```

The token is used to authenticate with the ClawHub registry when searching and installing skills. Without a valid token, skill installation will fail.

### Installing from ClawHub

```bash
# Install latest version
pulsebot skill install timeplus/sql-guide

# Install specific version
pulsebot skill install timeplus/sql-guide --version 1.2.0

# Install to custom directory
pulsebot skill install timeplus/sql-guide --dir /shared/skills
```

When you install a skill:
1. Downloads the skill ZIP from ClawHub registry
2. Validates only allowed text file types are present
3. Verifies SHA256 checksum matches the registry
4. Installs atomically (all-or-nothing)
5. Records the installation in `.clawhub/lock.json`
6. Scans the new skill directory and loads the skill

### Lock File (`.clawhub/lock.json`)

The lock file tracks ClawHub-installed skills with content hashes for integrity:

```json
{
  "version": 1,
  "skills": {
    "timeplus/sql-guide": {
      "slug": "timeplus/sql-guide",
      "version": "1.2.0",
      "content_hash": "sha256:abc123...",
      "installed_at": "2024-01-15T09:30:00Z",
      "source": "clawhub"
    }
  }
}
```

The lock file enables:
- **Integrity verification**: Detect if skill files were modified
- **Auto-updates**: Compare installed version with registry latest
- **Team synchronization**: Share `lock.json` to ensure consistent installations

### Auto-Updates

Enable automatic skill updates on startup:

```yaml
clawhub:
  auto_update: true
```

When enabled:
1. On startup, check all locked skills against ClawHub registry
2. If newer version available, download and install
3. Only updates if content hash differs (prevents unnecessary reinstalls)
4. Logs updates to console

### Allowed File Types

For security, ClawHub only allows text file types. Binary files (images, executables, etc.) are rejected during installation:

**Allowed extensions**: `.md`, `.txt`, `.yaml`, `.yml`, `.json`, `.toml`, `.js`, `.mjs`, `.cjs`, `.ts`, `.jsx`, `.tsx`, `.py`, `.sh`, `.bash`, `.css`, `.html`, `.svg`, `.xml`, `.csv`, `.ini`, `.cfg`, `.conf`, `.env`, `.gitignore`, `.editorconfig`, `.rs`, `.go`, `.java`, `.c`, `.cpp`, `.h`, `.hpp`, `.rb`, `.php`, `.swift`, `.kt`, `.scala`, `.sql`, `.r`, `.R`, `.jl`, `.lua`, `.pl`, `.pm`

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
| Skills with runtime dependencies (binaries, env vars) | OpenClaw-compatible skill |
| Share skills via registry | ClawHub-published skill |
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
- For OpenClaw skills, check requirement checker warnings

**`load_skill` / `read_skill_file` tools not available**:
- These only appear when at least one external skill is discovered
- Verify `skill_dirs` is configured and contains valid skill packages

**"Unknown built-in skill" error**:
- Check that the skill name matches one of: `file_ops`, `shell`, `workspace`

**Tool not being called by LLM**:
- Check tool description is clear and specific
- Ensure parameter schema is correct JSON Schema
- Verify tool name is unique across all skills

**ClawHub install fails**:
- Check network connectivity to `https://clawhub.ai`
- Verify the skill slug exists in the registry
- Ensure `--dir` points to a writable directory
- Check for disallowed file type errors (only text files allowed)

**Skill requirements not satisfied**:
- Check logs for specific missing binaries or env vars
- Verify required binaries are in PATH
- Set missing environment variables
- Use `always: true` in OpenClaw metadata to bypass checks (with caution)
