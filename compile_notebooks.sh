#!/bin/bash
set -e

# Check for --student flag
STUDENT_VERSION=false
if [[ "$1" == "--student" ]]; then
  STUDENT_VERSION=true
  echo "Generating STUDENT version (solutions removed)."
fi

# Directories to process
dirs=("exercises" "labs")

for dir in "${dirs[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "Directory $dir not found, skipping."
    continue
  fi

  echo "Compiling notebooks in $dir..."

  # Go into the directory to keep paths relative as jupytext expects or as previous scripts did
  pushd "$dir" >/dev/null

  # Loop over python files in src/
  for f in src/*.py; do
    # Check if file exists (in case glob matches nothing)
    [ -e "$f" ] || continue

    filename=$(basename "$f")
    temp_file="src/${filename}.temp.py"
    # Output to the current directory (which is exercises/ or labs/), using the filename without .py extension
    output_ipynb="${filename%.py}.ipynb"

    echo "  Converting $f -> $output_ipynb"

    # Only uncomment specific magics: # %pip, # %restart, # %writefile, # %write_and_run
    # We use a unified regex that covers both exercises and labs requirements
    sed -E 's/^# %(%?)(pip|restart|writefile|write_and_run)/%\1\2/g' "$f" >"$temp_file"

    # If student version, strip solutions from the temp file
    if [ "$STUDENT_VERSION" = true ]; then
      python3 -c "
          import re
          import sys

          file_path = '$temp_file'
          try:
          with open(file_path, 'r') as f:
          content = f.read()

          def replacer(match):
          indent = match.group(1)
          # Align pass and markers with the captured indentation
          # We include the solution markers as comments so students see where to fill in
          return f'{indent}# <solution>\n{indent}# TODO: Implement this\n{indent}pass\n{indent}# </solution>'

    # Pattern: ^([ \t]*) captures indentation at start of line
    pattern = r'^([ \t]*)# <solution>.*?# </solution>'

    new_content, count = re.subn(pattern, replacer, content, flags=re.DOTALL | re.MULTILINE)

    with open(file_path, 'w') as f:
    f.write(new_content)

    except Exception as e:
    print(f'Error stripping solutions from {file_path}: {e}', file=sys.stderr)
    sys.exit(1)
    "
    fi

    # Convert using percent format
    uvx jupytext --to ipynb "$temp_file" -o "$output_ipynb"

    # Clean up
    rm "$temp_file"
  done

  popd >/dev/null
done
