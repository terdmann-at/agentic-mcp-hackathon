#!/bin/bash
# solve_exercises.sh
# Copies the annotated solution files from .solutions/mas/ to src/deep_research/mas/

echo "Restoring solutions from .solutions/mas..."

# Copy key files
cp .solutions/mas/graph.py src/deep_research/mas/graph.py
cp .solutions/mas/nodes.py src/deep_research/mas/nodes.py

echo "Copying simple_agent solutions..."
cp .solutions/simple_agent/nodes.py src/deep_research/simple_agent/nodes.py
cp .solutions/simple_agent/graph.py src/deep_research/simple_agent/graph.py

# cp .solutions/mas/state.py src/deep_research/mas/state.py # Assuming state doesn't change

echo "Done. Solutions are now active in src/deep_research/mas/"
