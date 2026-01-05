from langchain_community.tools import DuckDuckGoSearchRun

# Define the tools our agent can use
search_tool = DuckDuckGoSearchRun()
tools = [search_tool]
