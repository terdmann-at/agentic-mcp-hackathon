from langchain_community.tools import DuckDuckGoSearchRun

# --- Exercise 2: Define Tools ---
# Goal: Initialize the tools that the agent will use.
# For deep research, we need a way to access the internet.

# We use DuckDuckGoSearchRun as a free, easy-to-setup search tool.
# In a real production system, you might use Tavily or Serper.

# search_tool = DuckDuckGoSearchRun()
search_tool = None

def get_tools():
    # TODO: Return the list of tools
    return []
