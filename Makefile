
all: 2026-01-21_agents-mcp-workshop.pdf

2026-01-21_agents-mcp-workshop.pdf: src/*.typ
	bash compile.sh
