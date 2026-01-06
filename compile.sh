#!/bin/bash
# Compile the Typst slides, setting the project root to the current directory
# and outputting the PDF to main.pdf in the root folder.

typst compile --root . src/main.typ 2026-01-21_agents-mcp-workshop.pdf
echo "Compiled main.pdf"
