#!/bin/bash
# solve_exercises.sh
# Copies the annotated solution files from .solutions/mas/ to src/deep_research/mas/

echo "Restoring solutions from .solutions/mas..."

# Copy key files
cp .solutions/mas/graph.py src/deep_research/mas/graph.py
cp .solutions/mas/nodes.py src/deep_research/mas/nodes.py

echo "Copying react solutions..."
cp .solutions/react/nodes.py src/deep_research/react/nodes.py
cp .solutions/react/graph.py src/deep_research/react/graph.py

# cp .solutions/mas/state.py src/deep_research/mas/state.py # Assuming state doesn't change

echo "Done. Solutions are now active in src/deep_research/mas/"
