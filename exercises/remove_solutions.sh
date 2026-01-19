#!/bin/bash
# remove_solutions.sh
# Removes code between # <solution> and # </solution> markers in exercises/*.py files

# Check for OS to handle sed inline quirks (macOS vs Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
  SED_CMD="sed -i ''"
else
  SED_CMD="sed -i"
fi

# Find all .py files in the current directory (maxdepth 1)
# avoiding directories like .solutions or lab_*
FILES=(src/*.py)

echo "Stripping solutions from: ${FILES[*]}"

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    # Using python for robust multi-line replacement as in the lab script
    python3 -c "
import sys
import re

file_path = '$file'
try:
    with open(file_path, 'r') as f:
        content = f.read()

    def replacer(match):
        indent = match.group(1)
        # Align pass and markers with the captured indentation
        return f'{indent}# <solution>\n{indent}# TODO: Implement this\n{indent}pass\n{indent}# </solution>'

    # Pattern: ^([ \t]*) captures indentation at start of line
    # The pattern matches: start of line, optional indentation, # <solution>, any content (non-greedy), # </solution>
    pattern = r'^([ \t]*)# <solution>.*?# </solution>'

    new_content, count = re.subn(pattern, replacer, content, flags=re.DOTALL | re.MULTILINE)

    with open(file_path, 'w') as f:
        f.write(new_content)
    
    if count > 0:
        print(f'Cleaned {count} blocks in {file_path}')
    else:
        print(f'No solution blocks found in {file_path} (unchanged)')

except Exception as e:
    print(f'Error processing {file_path}: {e}')
"
  else
    echo "Warning: $file not found"
  fi
done

echo "Done. Solutions removed."
