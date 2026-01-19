#!/bin/bash
# solve_exercises.sh
# Copies the full solution files from .solutions/ to exercises/ (root)

echo "Restoring solutions from .solutions/..."

# Copy all .py files from .solutions/ to current directory
# Assuming this script is run from exercises/ directory or we adjust paths
# Let's assume it's run from the exercises/ directory as per the file location
# But user might run it from root. The other scripts were in the lab folder.
# Let's make it robust to where it is run, or assume it's run from exercises/ dir if user cds there.
# The user's request implies "same structure", so generally scripts are run from the directory they are in.

cp .solutions/*.py src/

echo "Done. Solutions are now active in exercises/"
