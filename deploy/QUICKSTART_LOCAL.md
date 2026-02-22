# Local Quick Start Guide

This guide will walk you through setting up PulseBot locally using [Ollama](https://ollama.com/) for local models and Docker for the core services.

## 1. Install and Run Ollama

Ollama allows you to run large language models locally on your machine.

1.  **Download Ollama**: Visit [ollama.com](https://ollama.com/) and follow the installation instructions for your OS.
2.  **Pull Required Models**:
    Open your terminal and run the following commands.
    
    > [!IMPORTANT]
    > To use the `kimi-k2.5:cloud` model, you must first log in to your Ollama account:
    > ```bash
    > ollama login
    > ```

    Then pull the models for the agent and its memory:
    ```bash
    # For the Agent LLM (Kimi via Ollama)
    ollama pull kimi-k2.5:cloud

    # For the Agent Memory (Embeddings)
    ollama pull mxbai-embed-large
    ```
3.  **Start Ollama**: Ensure the Ollama server is running (usually it starts automatically after installation).


## 3. Run with Docker Compose

PulseBot provides pre-configured Docker environments. For a simple local setup, use the Proton (open-source) version.

1.  **Navigate to the deployment folder**:
    ```bash
    cd deploy/proton
    ```
2.  **Start the services**:
    ```bash
    docker-compose up -d
    ```

This will start:
- **Proton**: The streaming database (available at ports 8123, 3218, 8463).
- **PulseBot Agent**: Connected to your local Ollama instance.

### Verification
Once the services are up, you can access the PulseBot Web UI at:
`http://localhost:8001`

For more detailed configuration options, see [docs/configuration.md](../docs/configuration.md).
