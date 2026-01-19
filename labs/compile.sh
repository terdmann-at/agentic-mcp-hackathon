#!/bin/bash

for f in src/*.py; do

  filename=$(basename "$f")
  temp_file="src/${filename}.temp.py"
  # Output to the root directory (current dir), using the filename without .py extension
  output_ipynb="${filename%.py}.ipynb"

  # Only uncomment specific magics: # %pip and # %restart
  sed -E 's/^# %(%?)(pip|restart|writefile|write_and_run)/%\1\2/g' "$f" >"$temp_file"

  # Convert using percent format
  uvx jupytext --to ipynb "$temp_file" -o "$output_ipynb"

  # Clean up
  rm "$f.temp.py"
done
