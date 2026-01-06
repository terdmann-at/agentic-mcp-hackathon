from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from deep_research.mas.state import ResearchState
from deep_research.mas.nodes import chief_editor_node, research_worker_node, writer_node


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
# Initialize Graph
workflow = StateGraph(ResearchState)

# Add Nodes
workflow.add_node("chief_editor", chief_editor_node)
workflow.add_node("research_worker", research_worker_node)
workflow.add_node("writer", writer_node)

# Add Edges
# Start -> Chief Editor
workflow.add_edge(START, "chief_editor")

# Chief Editor -> Parallel Workers (Map)
workflow.add_conditional_edges("chief_editor", map_subtopics, ["research_worker"])

# Workers -> Writer (Reduce)
# The "research_worker" node output will be automatically appended to "research_outputs"
# because we annotated it with operator.add in ResearchState.
workflow.add_edge("research_worker", "writer")

# Writer -> End
workflow.add_edge("writer", END)

# Compile
mas_app = workflow.compile()
# </solution>
