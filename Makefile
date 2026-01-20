.PHONY: all slides notebooks

all: slides notebooks

slides:
	typst compile --root . src/main.typ 2026-01-21_agents-mcp-workshop.pdf

notebooks:
	bash compile_notebooks.sh

notebooks-student:
	bash compile_notebooks.sh --student
