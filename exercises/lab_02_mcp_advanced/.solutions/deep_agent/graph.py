from typing import Literal

from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from mcp_agent.tools.web_search import web_search

from .fs_tools import fs_tools
from .state import AgentState
from .subagent import subagent_tools
from .todo_tools import todo_tools

# 1. Setup Tools
# The main agent has access to all tools
# It uses 'task' to delegate, 'write_todos' to plan, 'fs_*' for files.
all_tools = fs_tools + todo_tools + subagent_tools + [web_search]


# 2. Nodes
def agent_node(state: AgentState):
    model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
    model = model.bind_tools(all_tools)

    # Optional: Add system prompt if not present
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        system_prompt = SystemMessage(
            content="""You are a Deep Research Agent.
You have access to a virtual filesystem, a todo list manager, and the ability to spawn sub-agents.

CORE WORKFLOW:
1. ALWAYS start by creating a plan using `write_todos`.
2. Iterate through your todo list.
   - Use `task` to delegate complex steps to sub-agents.
   - Use `web_search` for quick lookups.
   - Use filesystem tools to read/write persistent context.
3. Update your todo list status as you progress using `mark_todo_completed`.
4. When detailed research is needed, assign it to a sub-agent with specific instructions.
5. Compile your final answer from the files or context.
"""
        )
        messages = [system_prompt] + messages

    response = model.invoke(messages)
    return {"messages": [response]}


async def tools_node_with_state_update(state: AgentState):
    """Executes tools and updates state for special tools like write_todos."""
    # We use the standard ToolNode for execution, but we wrap it/logic here
    # primarily to intercept state updates.

    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return {}  # Should not happen if routed here

    # Execute tools
    tool_node = ToolNode(all_tools)
    result = await tool_node.ainvoke(state)

    # State Updates interception
    new_state_updates = {"messages": result["messages"]}

    for tool_call in last_message.tool_calls:
        if tool_call["name"] == "write_todos":
            # Update the todo list in the state
            todos_args = tool_call["args"].get("todos", [])
            new_todos = [
                {"task": t, "status": "pending", "subtasks": []} for t in todos_args
            ]
            new_state_updates["todos"] = new_todos
            new_state_updates["current_todo_index"] = 0

        elif tool_call["name"] == "mark_todo_completed":
            idx = tool_call["args"].get("index")
            if idx is not None and "todos" in state:
                # We need to copy the list to modify it
                todos = list(state["todos"])
                if 0 <= idx < len(todos):
                    todos[idx]["status"] = "completed"
                    new_state_updates["todos"] = todos

                    # Update current index
                    next_idx = idx + 1
                    if next_idx < len(todos):
                        new_state_updates["current_todo_index"] = next_idx
                    else:
                        new_state_updates["current_todo_index"] = None

    return new_state_updates


# 3. Routing
def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"


# <solution>
# 4. Graph Construction
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", tools_node_with_state_update)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
# </solution>
