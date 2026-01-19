#!/bin/bash
set -e

# Directories to process
dirs=("exercises" "labs")

for dir in "${dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Directory $dir not found, skipping."
        continue
    fi

    echo "Compiling notebooks in $dir..."
    
    # Go into the directory to keep paths relative as jupytext expects or as previous scripts did
    pushd "$dir" > /dev/null

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

        # Convert using percent format
        uvx jupytext --to ipynb "$temp_file" -o "$output_ipynb"

        # Clean up
        rm "$temp_file"
    done

    popd > /dev/null
done
