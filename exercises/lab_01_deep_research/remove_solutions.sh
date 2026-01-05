#!/bin/bash
# remove_solutions.sh
# Removes code between # <solution> and # </solution> markers in src/deep_research/mas/ files

# Check for OS to handle sed inline quirks (macOS vs Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
  SED_CMD="sed -i ''"
else
  SED_CMD="sed -i"
fi

FILES=(
  "src/deep_research/mas/graph.py"
  "src/deep_research/mas/nodes.py"
  "src/deep_research/react_agent.py"
)

echo "Stripping solutions from: ${FILES[*]}"

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    # Delete lines between # <solution> and # </solution> exclusive
    # Note: This simple sed logic deletes the markers too?
    # User asked to "delete the code between <solution> and </solution>".
    # Usually we want to Keep the markers so the student sees where to type, or remove them entirely?
    # If we keep markers, we can use: sed '/# <solution>/,/# <\/solution>/ { /# <solution>/b; /# <\/solution>/b; d; }'
    
    # Using python for safety and clarity as discussed
    python3 -c "
import sys
import re

file_path = '$file'
with open(file_path, 'r') as f:
    content = f.read()

# Pattern: # <solution> ... # </solution>
# flags=re.DOTALL matches newline
new_content = re.sub(r'# <solution>.*?# </solution>', '# <solution>\n    # TODO: Implement this\n    pass\n    # </solution>', content, flags=re.DOTALL)

with open(file_path, 'w') as f:
    f.write(new_content)
"
    echo "Cleaned $file"
  else
    echo "Warning: $file not found"
  fi
done

echo "Done. Solutions removed."
