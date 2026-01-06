#!/bin/bash
# remove_solutions.sh

echo "Resetting exercises from .exercises..."

# Check for OS to handle sed inline quirks (macOS vs Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
  SED_CMD="sed -i ''"
else
  SED_CMD="sed -i"
fi

FILES=(
  "src/mcp_agent/coding_agent/agent.py"
  "src/mcp_agent/deep_agent/graph.py"
  "src/mcp_agent/deep_agent/coding_subagent.py"
)

echo "Stripping solutions from: ${FILES[*]}"

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    # Using python for safety and clarity
    python3 -c "
import sys
import re

file_path = '$file'
with open(file_path, 'r') as f:
    content = f.read()

def replacer(match):
    indent = match.group(1)
    # Align pass and markers with the captured indentation
    return f'{indent}# <solution>\n{indent}# TODO: Implement this\n{indent}pass\n{indent}# </solution>'

# Pattern: ^([ \t]*) captures indentation at start of line
# flags=re.DOTALL | re.MULTILINE
pattern = r'^([ \t]*)# <solution>.*?# </solution>'

new_content = re.sub(pattern, replacer, content, flags=re.DOTALL | re.MULTILINE)

with open(file_path, 'w') as f:
    f.write(new_content)
"
    echo "Cleaned $file"
  else
    echo "Warning: $file not found"
  fi
done

echo "Done. Exercises are reset."
