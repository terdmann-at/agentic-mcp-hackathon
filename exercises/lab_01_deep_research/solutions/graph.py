# --- Exercise 4: Define the Graph ---
# Goal: Wire the nodes together into a runnable graph.

from langgraph.graph import StateGraph, START, END
from src.state import ResearchState
from src.nodes import planner_node, searcher_node, synthesizer_node

# 1. Initialize the Graph with our State
workflow = StateGraph(ResearchState)

# 2. Add Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("searcher", searcher_node)
workflow.add_node("synthesizer", synthesizer_node)

# 3. Add Edges
# Define the flow: Start -> Planner -> Searcher -> Synthesizer -> End
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "searcher")
workflow.add_edge("searcher", "synthesizer")
workflow.add_edge("synthesizer", END)

# 4. Compile the Graph
app = workflow.compile()
