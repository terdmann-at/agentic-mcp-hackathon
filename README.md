# Agentic AI and MCP Workshop

This repo contains the slides (typst source in `/src`) and exercises (see `exercises/` and `labs/`).

## Dependencies

* For the slides, you'll need `typst`: https://github.com/typst/typst
* For the notebooks, you'll need `uv`: https://docs.astral.sh/uv/getting-started/installation

Alternatively, if you don't want to install anything have docker, you can compile the notebooks by starting a docker container that has uv:

    docker run -v ".:/app" -w /app --rm -it ghcr.io/astral-sh/uv:debian bash

and running

    make notebooks

## Usage

### Slides

Use this to compile the slides:

    make slides

### Notebooks

The notebooks in `exercises/` are created via

    make notebooks

This takes the `.py` files and compiles them into `.ipynb` files. These will contain the solutions. If you want the exercises without solutions in the notebooks, use this:

    make notebooks-student

