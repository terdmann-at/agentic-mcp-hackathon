# --- Exercise 3: Define Nodes ---
# Goal: Implement the logic for each step in the research workflow.

from langchain_openai import AzureChatOpenAI
from deep_research.state import ResearchState, ResearchPlan
from deep_research.tools import search_tool


# Initialize the Model
# Adjust deployment_name if needed
llm = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)

def planner_node(state: ResearchState):
    """
    1. Identify the topic from the state.
    2. Use the LLM to generate a plan (3 structured sub-queries).
    3. Return the new 'sub_queries' list to update the state.
    """
    # TODO: Implement planner
    return {}

def searcher_node(state: ResearchState):
    """
    1. Read 'sub_queries' from state.
    2. For each query, execute the search_tool. 
    3. Return 'search_results' (which will be appended to the state list).
    """
    # TODO: Implement searcher
    return {}

def synthesizer_node(state: ResearchState):
    """
    1. Read accumulated 'search_results' from state.
    2. Ask the LLM to write a final report based on these results.
    3. Return 'summary'.
    """
    # TODO: Implement synthesizer
    return {}
