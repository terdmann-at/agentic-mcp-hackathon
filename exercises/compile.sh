#!/bin/bash

for f in src/*.py; do
  [ -e "$f" ] || continue

  filename=$(basename "$f")
  temp_file="src/${filename}.temp.py"
  
  # Output to the root directory (current dir), using the filename without .py extension
  output_ipynb="${filename%.py}.ipynb"

  # Only uncomment specific magics: # %pip and # %restart
  sed -E 's/^# %(%?)(pip|restart|writefile)/%\1\2/g' "$f" >"$temp_file"

  # Convert using percent format
  uvx jupytext --to ipynb "$temp_file" -o "$output_ipynb"

  # Clean up
  rm "$temp_file"
done
