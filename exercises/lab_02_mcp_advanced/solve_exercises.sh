#!/bin/bash
# solve_exercises.sh

echo "Restoring solutions from .solutions..."

# Coding Agent
cp .solutions/coding_agent/agent.py src/mcp_agent/coding_agent/agent.py

# Deep Agent
cp .solutions/deep_agent/graph.py src/mcp_agent/deep_agent/graph.py
cp .solutions/deep_agent/coding_subagent.py src/mcp_agent/deep_agent/coding_subagent.py

echo "Done. Solutions are now active."
