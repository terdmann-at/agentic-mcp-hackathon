# Lab 01: Deep Research

In this lab, you will build a multi-agent system for deep research.

## Structure

- `src/deep_research/mas`: Multi-agent system implementation.
- `src/deep_research/react_agent.py`: ReAct baseline agent.

## Setup

1. Install dependencies: `uv sync`
2. Run the UI: `uv run ui`

## Observability

This lab is instrumented with **MLflow** for tracing.

### 1. Run the Agents
Run the UI or the CLI main script:

```bash
uv run ui
# or
uv run python src/deep_research/main.py
```

### 2. View Traces
Start the MLflow UI in a new terminal window:

```bash
uv run mlflow ui --port 5001
```

Then open `http://localhost:5001` in your browser.
