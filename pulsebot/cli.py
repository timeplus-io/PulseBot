"""CLI interface for PulseBot."""

from __future__ import annotations

import asyncio
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="pulsebot")
def cli():
    """PulseBot - Stream-native AI Agent powered by Timeplus."""
    pass


@cli.command()
@click.option("--config", "-c", default="config.yaml", help="Config file path")
def run(config: str):
    """Start the PulseBot agent."""
    from pulsebot.config import load_config
    from pulsebot.core import Agent
    from pulsebot.factory import create_provider, create_skill_loader
    from pulsebot.skills import SkillLoader
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.embeddings import OpenAIEmbeddingProvider, OllamaEmbeddingProvider
    from pulsebot.timeplus.memory import MemoryManager
    from pulsebot.utils import setup_logging

    cfg = load_config(config)
    setup_logging(cfg.logging.level, cfg.logging.format)

    console.print(Panel.fit(
        f"[bold green]Starting PulseBot[/]\n"
        f"Agent: {cfg.agent.name}\n"
        f"Provider: {cfg.agent.provider}\n"
        f"Model: {cfg.agent.model}"
    ))

    async def main():
        # Initialize components
        tp = TimeplusClient.from_config(cfg.timeplus)

        provider = create_provider(cfg)

        # Create embedding provider based on memory configuration
        embedding_provider = None
        memory_cfg = cfg.memory

        if memory_cfg.enabled:
            if memory_cfg.embedding_provider == "openai":
                api_key = memory_cfg.embedding_api_key or cfg.providers.openai.api_key
                if api_key:
                    embedding_provider = OpenAIEmbeddingProvider(
                        api_key=api_key,
                        model=memory_cfg.embedding_model,
                        dimensions=memory_cfg.embedding_dimensions,
                    )
                    console.print(f"[dim]Using OpenAI embeddings: {memory_cfg.embedding_model}[/]")
                else:
                    console.print("[yellow]Warning: OpenAI embedding provider configured but no API key available[/]")
            elif memory_cfg.embedding_provider == "ollama":
                host = memory_cfg.embedding_host or cfg.providers.ollama.host
                try:
                    embedding_provider = OllamaEmbeddingProvider(
                        host=host,
                        model=memory_cfg.embedding_model,
                        dimensions=memory_cfg.embedding_dimensions,
                        timeout_seconds=memory_cfg.embedding_timeout_seconds,
                    )
                    console.print(f"[dim]Using Ollama embeddings: {memory_cfg.embedding_model} at {host}[/]")
                except Exception as e:
                    console.print(f"[yellow]Warning: Failed to initialize Ollama embedding provider: {e}[/]")
            else:
                console.print(f"[yellow]Warning: Unknown embedding provider: {memory_cfg.embedding_provider}[/]")

            if not embedding_provider:
                console.print("[yellow]Warning: Memory features disabled - no embedding provider available[/]")
        else:
            console.print("[dim]Memory system disabled in configuration[/]")

        # Create a separate client for memory operations to avoid
        # "Simultaneous queries on single connection" error
        memory_tp = TimeplusClient.from_config(cfg.timeplus)
        memory = MemoryManager(
            client=memory_tp,
            embedding_provider=embedding_provider,
            similarity_threshold=cfg.memory.similarity_threshold,
        )

        skills = create_skill_loader(cfg)
        
        workspace_skill = skills.get_skill("workspace")
        if workspace_skill is not None:
            from pulsebot.workspace import run_workspace_server
            asyncio.create_task(
                run_workspace_server(workspace_skill.manager, cfg.workspace, cfg.timeplus.username, cfg.timeplus.password, cfg.timeplus.host)
            )
            console.print(
                f"[dim]WorkspaceServer started on port {cfg.workspace.workspace_port}[/]"
            )

        agent = Agent(
            agent_id="main",
            timeplus=tp,
            llm_provider=provider,
            skill_loader=skills,
            memory_manager=memory,
            agent_name=cfg.agent.name,
            model_info=f"Model: {cfg.agent.model}\nProvider: {cfg.agent.provider}",
            timeplus_config=cfg.timeplus,
        )

        # Start Telegram channel if enabled (needs separate client to avoid connection conflicts)
        telegram_channel = None
        if cfg.channels.telegram.enabled and cfg.channels.telegram.token:
            from pulsebot.channels.telegram import TelegramChannel
            # Create dedicated Timeplus client for Telegram to avoid simultaneous query errors
            telegram_tp = TimeplusClient.from_config(cfg.timeplus)
            telegram_channel = TelegramChannel(
                token=cfg.channels.telegram.token,
                timeplus_client=telegram_tp,
                allowed_users=cfg.channels.telegram.allow_from or None,
            )
            await telegram_channel.start()
            console.print("[green]Telegram channel started[/]")

        console.print("[green]Agent running. Press Ctrl+C to stop.[/]")

        try:
            await agent.run()
        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down...[/]")
            if telegram_channel:
                await telegram_channel.stop()
            await agent.stop()
            if workspace_skill is not None:
                await workspace_skill.manager.shutdown_all()

    asyncio.run(main())


@cli.command()
@click.option("--config", "-c", default="config.yaml", help="Config file path")
@click.option("--host", default="0.0.0.0", help="API server host")
@click.option("--port", default=8000, help="API server port")
def serve(config: str, host: str, port: int):
    """Start the PulseBot API server."""
    import uvicorn
    from pulsebot.config import load_config
    from pulsebot.utils import setup_logging

    cfg = load_config(config)
    setup_logging(cfg.logging.level, cfg.logging.format)

    console.print(Panel.fit(
        f"[bold green]Starting PulseBot API[/]\n"
        f"Host: {host}:{port}\n"
        f"Docs: http://{host}:{port}/docs"
    ))
    
    console.print(f"[dim]Workspace agent_base_url: {cfg.workspace.agent_base_url}[/]")

    uvicorn.run(
        "pulsebot.api:create_app",
        host=host,
        port=port,
        factory=True,
        reload=False,
    )


@cli.command()
@click.option("--host", default="localhost", help="API server host")
@click.option("--port", default=8000, help="API server port")
def chat(host: str, port: int):
    """Interactive chat with PulseBot via API."""
    import httpx
    import json
    import uuid
    import websockets
    from rich.markdown import Markdown

    console.print(Panel.fit(
        f"[bold green]PulseBot Interactive Chat[/]\n"
        f"Connected to http://{host}:{port}\n"
        "Type 'exit' or 'quit' to end session"
    ))

    session_id = str(uuid.uuid4())
    api_url = f"http://{host}:{port}"
    ws_url = f"ws://{host}:{port}/ws/{session_id}"

    async def chat_loop():
        # Check if API is healthy
        try:
            async with httpx.AsyncClient() as client:
                await client.get(f"{api_url}/health")
        except Exception:
            console.print(f"[red]Error: Could not connect to PulseBot API at {api_url}[/]")
            console.print("Make sure the agent is running: [bold]docker compose up -d[/]")
            return

        try:
            async with websockets.connect(ws_url) as websocket:
                console.print(f"[dim]Connected to session: {session_id}[/]\n")

                # Event to signal when response is received
                response_received = asyncio.Event()

                # Track active tool calls for display
                active_tools = {}

                # Task to receive messages
                async def receive_messages():
                    try:
                        while True:
                            message = await websocket.recv()
                            data = json.loads(message)

                            if data.get("type") == "tool_call":
                                tool_name = data.get("tool_name", "unknown")
                                status = data.get("status", "")
                                args_summary = data.get("args_summary", "")

                                if status == "started":
                                    if args_summary:
                                        console.print(f" [dim cyan]⚙[/] [bold]{tool_name}[/] [dim]{args_summary}[/]")
                                    else:
                                        console.print(f" [dim cyan]⚙[/] [bold]{tool_name}[/]")
                                    active_tools[tool_name] = True
                                else:
                                    duration = data.get("duration_ms", 0)
                                    if status == "success":
                                        console.print(f" [dim green]✓ {tool_name}[/] [dim]({duration}ms)[/]")
                                    else:
                                        console.print(f" [dim red]✗ {tool_name} failed[/]")
                                    active_tools.pop(tool_name, None)

                            elif data.get("type") == "response":
                                response_text = data.get("text", "")
                                console.print(Panel(
                                    Markdown(response_text),
                                    title="[bold green]PulseBot[/]",
                                    border_style="green",
                                ))
                                response_received.set()
                    except websockets.exceptions.ConnectionClosed:
                        pass

                receive_task = asyncio.create_task(receive_messages())

                while True:
                    try:
                        user_input = await asyncio.get_event_loop().run_in_executor(
                            None, console.input, "[bold blue]You>[/] "
                        )

                        if user_input.lower() in ("exit", "quit", "q"):
                            console.print("[yellow]Goodbye![/]")
                            break

                        if not user_input.strip():
                            continue

                        # Clear the event before sending
                        response_received.clear()

                        await websocket.send(json.dumps({
                            "type": "message",
                            "text": user_input
                        }))

                        # Show waiting indicator and wait for response
                        with console.status("[dim]Thinking...[/]", spinner="dots"):
                            try:
                                await asyncio.wait_for(response_received.wait(), timeout=60)
                            except asyncio.TimeoutError:
                                console.print("[yellow]Response timed out[/]")

                    except KeyboardInterrupt:
                        console.print("\n[yellow]Goodbye![/]")
                        break

                receive_task.cancel()

        except Exception as e:
            console.print(f"[red]Connection error: {e}[/]")

    # Run the async loop
    try:
        asyncio.run(chat_loop())
    except KeyboardInterrupt:
        pass





@cli.command()
@click.option("--config", "-c", default="config.yaml", help="Config file path")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation")
def reset(config: str, force: bool):
    """Reset PulseBot data by recreating all streams."""
    from pulsebot.config import load_config
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.timeplus.setup import create_streams, drop_streams

    if not force:
        if not click.confirm(
            "Are you sure you want to delete all PulseBot data? This cannot be undone."
        ):
            console.print("[yellow]Cancelled.[/]")
            return

    cfg = load_config(config)

    console.print("[bold red]Resetting PulseBot infrastructure...[/]")

    async def run_reset():
        tp = TimeplusClient.from_config(cfg.timeplus)
        
        # Drop existing streams
        await drop_streams(tp)
        
        # Recreate streams
        console.print("Recreating Timeplus streams...")
        await create_streams(tp)
        console.print("[green]✓ Timeplus streams recreated[/]")

    asyncio.run(run_reset())
    console.print("\n[bold green]Reset complete![/]")


@cli.command()
def init():
    """Generate default config.yaml."""
    from pulsebot.config import generate_default_config

    config_path = "config.yaml"

    import os
    if os.path.exists(config_path):
        if not click.confirm(f"{config_path} already exists. Overwrite?"):
            console.print("[yellow]Cancelled.[/]")
            return

    content = generate_default_config()

    with open(config_path, "w") as f:
        f.write(content)

    console.print(f"[green]Created {config_path}[/]")
    console.print("Edit the file and set your API keys and connection details.")


@cli.group()
def task():
    """Manage scheduled tasks."""
    pass


@task.command("list")
@click.option("--config", "-c", default="config.yaml", help="Config file path")
def list_tasks(config: str):
    """List all scheduled tasks."""
    from pulsebot.config import load_config
    from pulsebot.timeplus.client import TimeplusClient
    from pulsebot.timeplus.tasks import TaskManager

    cfg = load_config(config)
    tp = TimeplusClient.from_config(cfg.timeplus)
    task_mgr = TaskManager(tp)

    tasks = task_mgr.list_tasks()

    if not tasks:
        console.print("[yellow]No tasks found.[/]")
        return

    from rich.table import Table

    table = Table(title="Scheduled Tasks")
    table.add_column("Name")
    table.add_column("Schedule")
    table.add_column("Status")

    for t in tasks:
        table.add_row(
            t.get("name"),
            t.get("schedule"),
            "[green]Running[/]" if t.get("running") else "[red]Paused[/]"
        )

    console.print(table)


if __name__ == "__main__":
    cli()
