# Lab 02: MCP Advanced - Coding & Deep Agents

In this lab, you will build an advanced agent system consisting of:
1.  **Coding Agent**: A ReAct agent capable of executing Python code in a safe Docker sandbox.
2.  **Deep Agent**: A LangGraph-based agent that performs research and delegates complex tasks to sub-agents (like the Coding Agent).

## Structure
- `src/mcp_agent/coding_agent`: Contains the Coding Agent implementation.
  - `agent.py`: **[EXERCISE]** You will define the system prompt and build the ReAct agent here.
- `src/mcp_agent/deep_agent`: Contains the Deep Agent implementation.
  - `graph.py`: **[EXERCISE]** You will define the LangGraph state graph here (nodes and edges).
  - `coding_subagent.py`: **[EXERCISE]** You will implement the `delegate_code_task` tool to wrap the Coding Agent.

## Setup
Ensure you have the environment set up (uv, docker).

## Exercises

### Part 1: Coding Agent
**Goal**: Implement a ReAct agent that uses Sequential Thinking, Docker, and Web Search.
1.  Open `src/mcp_agent/coding_agent/agent.py`.
2.  Implement the `build_agent` function.
    - Define a powerful system prompt (mention Sequential Thinking and Docker).
    - Use `create_react_agent` to build and return the agent.

**Verification**:
Run the Coding Agent test:
```bash
uv run pytest tests/test_coding_agent.py
```

### Part 2: Deep Agent & Sub-Agent Integration
**Goal**: Build a Deep Agent that can delegate code tasks.
1.  Open `src/mcp_agent/deep_agent/graph.py`.
    - Build the `StateGraph` with `agent` and `tools` nodes.
    - Wire them up with standard ReAct edges (START -> agent -> tools -> agent).
2.  Open `src/mcp_agent/deep_agent/coding_subagent.py`.
    - Implement `delegate_code_task`.
    - It must establish connections to Docker (SSE) and Sequential Thinking (Stdio).
    - Build and run the `coding_agent` within this isolated scope.

**Verification**:
Run the Deep Agent integration test (Hard GAIA Question):
```bash
uv run pytest tests/test_gaia.py
```

## Observability

This lab is instrumented with **MLflow** for tracing. You can inspect the internal steps, tool calls, and model interactions of your agents.

### 1. Run the Agents
Run your agents as usual. Traces will be automatically captured.

```bash
uv run deep-agent
```

### 2. View Traces
Start the MLflow UI in a new terminal window:

```bash
uv run mlflow ui --port 5001
```

Then open `http://localhost:5001` in your browser.

## Solutions
To see the answers or skip ahead:
```bash
./solve_exercises.sh
```

To reset to the exercise state:
```bash
./remove_solutions.sh
```
