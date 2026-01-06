from langgraph.graph import StateGraph, START, END
from deep_research.react.state import AgentState
from deep_research.react.nodes import call_model, tool_node, should_continue

# Exercise: Wire the ReAct Graph
# 1. Initialize StateGraph with AgentState.
# 2. Add nodes: "agent" (call_model) and "tools" (tool_node).
# 3. Add edge: START -> "agent".
# 4. Add conditional edge: "agent" -> should_continue -> ["tools", END].
# 5. Add edge: "tools" -> "agent".
# 6. Compile to 'app'.
# <solution>
# Initialize Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Add Edges
# Start at the agent
workflow.add_edge(START, "agent")

# Conditional edge from agent: 'tools' or END
workflow.add_conditional_edges("agent", should_continue, ["tools", END])

# Loop back from tools to agent
workflow.add_edge("tools", "agent")

# Compile
app = workflow.compile()
# </solution>
