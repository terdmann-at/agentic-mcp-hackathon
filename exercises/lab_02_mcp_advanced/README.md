# Lab 2: Advanced MCP Multi-Agent System

This lab builds an advanced agentic system that combines:
1.  **Safe Code Execution**: Using a local Docker-based MCP server.
2.  **Advanced Reasoning**: Using the `@modelcontextprotocol/server-sequential-thinking` MCP server.
3.  **Web Research**: Using a custom local tool to scrape web pages.

## Setup

1.  **Prerequisites**:
    *   Docker Desktop must be running.
    *   `uv` installed.
    *   `npx` installed (Node.js).

2.  **Install Dependencies**:
    Dependencies are managed via `uv` in `pyproject.toml`.
    ```bash
    uv sync
    ```

## Structure

*   `src/main.py`: The entry point. Connects to MCP servers and runs the agent.
*   `src/mcp_server_docker.py`: A local MCP server that wraps `docker run` to execute Python code safely.
*   `src/tools/web_search.py`: A simple tool to fetch and markdownify web pages.

## Running the Lab

Run the main agent script:

```bash
uv run src/main.py
```

## Tasks for the Lab

1.  **Analyze the Architecture**: Look at how `src/main.py` connects to multiple MCP servers using `stdio_client`.
2.  **Test the Agent**: Try asking it complex questions that require planning, coding, and searching.
    *   *Example*: "Research the performance of the latest Llama 3 models, then create a plot comparing them to GPT-4 based on public benchmarks."
3.  **Convert to Multi-Agent**:
    *   Currently, `src/main.py` uses a single ReAct agent with all tools.
    *   **Challenge**: Refactor `src/main.py` to use a **Supervisor** pattern (using LangGraph) with two distinct workers:
        *   `Researcher`: Has access to `web_search` and `sequential_thinking`.
        *   `Coder`: Has access to `execute_python`.
        *   The Supervisor routes tasks between them.

## Troubleshooting

*   **Docker Errors**: Ensure Docker is running. The first run might take 10-20s to pull the `uv` image.
*   **Sequential Thinking Error**: Ensure `npx` is available in your PATH.
