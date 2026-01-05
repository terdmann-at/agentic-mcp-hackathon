from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from solutions.mas.state import ResearchState, SubTaskState
from solutions.mas.nodes import chief_editor_node, research_worker_node, writer_node

def map_subtopics(state: ResearchState):
    """
    Conditional edge function that maps sub-topics to parallel worker calls.
    Returns a list of Send objects.
    """
    return [
        Send("research_worker", {"topic": sub_topic}) 
        for sub_topic in state["sub_topics"]
    ]

# Exercise: Define the Graph
# 1. Initialize StateGraph with ResearchState
# 2. Add nodes: "chief_editor", "research_worker", "writer"
# 3. Add edges: START -> chief_editor -> map_subtopics (conditional) -> writer -> END
# 4. Compile the graph to 'mas_app'
# <solution>
    # TODO: Implement this
    pass
    # </solution>
