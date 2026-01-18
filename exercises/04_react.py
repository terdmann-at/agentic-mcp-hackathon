# %% [markdown]
# # Exercise 4: ReAct Agent
#
# Goal: Build a ReAct agent from scratch using LangGraph.
# Expected time: 15 min
#

# %%
# %pip install databricks-langchain langchain-community ddgs langgraph
# %restart_python

# %%
import operator
from typing import Literal

from databricks_langchain import ChatDatabricks
from langchain.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import BaseTool, tool
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict

# %%
model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5")


# %%
# Tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`.Args: a: First int, b: Second int"""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`.Args: a: First int, b: Second int"""
    return a + b


# Exercise 4.1: Define the divide tool
# Hint: Use the @tool decorator. The function should take two ints and return a float.
# <solution>
@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.Args: a: First int, b: Second int"""
    return a / b


# </solution>

# %% [markdown]
# ## Web search
#
# Let's also try adding another interesting tool: web search.
#
#

# %%
# the agent will have these tools
tools = [add, multiply, divide]


def build_agent(tools: list[BaseTool]):
    tools_by_name = {tool.name: tool for tool in tools}
    model_with_tools = model.bind_tools(tools)

    # State
    class MessagesState(TypedDict):
        messages: Annotated[list[AnyMessage], operator.add]
        llm_calls: int

    # Nodes
    def llm_call(state: dict):
        """LLM decides whether to call a tool or not"""
        return {
            "messages": [
                model_with_tools.invoke(
                    [
                        SystemMessage(
                            content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                        )
                    ]
                    + state["messages"]
                )
            ],
            "llm_calls": state.get("llm_calls", 0) + 1,
        }

    def tool_node(state: dict):
        """Performs the tool call"""
        result = []
        for tool_call in state["messages"][-1].tool_calls:
            # Exercise 4.2: Handle the tool call. That is, call the function with the arguments
            # requested by the LLM and add the result (as a `ToolMessage`) to the conversation history.
            # <solution>
            tool = tools_by_name[tool_call["name"]]
            observation = tool.invoke(tool_call["args"])
            result.append(
                ToolMessage(content=observation, tool_call_id=tool_call["id"])
            )
            # </solution>
        return {"messages": result}

    # Exercise 4.3: Define conditional logic
    # Hint: Check if the last message in state["messages"] has `tool_calls`.
    def should_continue(state: MessagesState) -> Literal["tool_node", END]:
        """Decide if we should continue the loop or stop"""
        messages = state["messages"]
        last_message = messages[-1]
        # <solution>
        if last_message.tool_calls:
            return "tool_node"
        return END
        # </solution>

    # %%
    # Exercise 4.4: Initialize graph and add nodes
    # Hint: Use StateGraph(MessagesState). Add nodes using .add_node("name", function).
    # <solution>
    agent_builder = StateGraph(MessagesState)
    agent_builder.add_node("llm_call", llm_call)
    agent_builder.add_node("tool_node", tool_node)
    # </solution>

    # Exercise 4.5: Add edges
    # Hint: Use .add_edge(start, end) and .add_conditional_edges(source, condition, path_map).
    # Connect START -> llm_call, then conditionally to tool_node or END, and tool_node back to llm_call.
    # <solution>
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
    agent_builder.add_edge("tool_node", "llm_call")
    # </solution>

    return agent_builder.compile()


# Exercise 4.6: Compile the graph
# Hint: Call .compile() on the graph builder.
# <solution>
agent = build_agent(tools)
# </solution>


# %%
# Let's run this query
math_query = "Calculate ((144 / 12) * (25 + 75)) / ((10 * 10) / (500 / 5)) + ((81 / 9) * (121 / 11))"

# Exercise 4.7: Invoke the agent.
# Hint: Initialize the conversation history with the query wrapped in a `HumanMessage` and use agent.invoke({"messages": messages})
# <solution>
messages = [HumanMessage(content=math_query)]
response = agent.invoke({"messages": messages})
# </solution>

# show the message history
for m in response["messages"]:
    m.pretty_print()


# %%
# Exercise 4.8: Create another agent, with the ability to search the web.
#
from ddgs import DDGS


# Exercise 4.9: Use the above to create a search tool
# <solution>
@tool
def web_search(query: str, max_results: int = 5):
    """Run a web search"""
    return DDGS().text(query, max_results=max_results)


# </solution>

# %%
search_query = "What is Altana?"
# Exercise 4.10: Build and invoke the agent.
# <solution>
agent = build_agent([web_search])
messages = [HumanMessage(content=search_query)]
response = agent.invoke({"messages": messages})
# </solution>

for m in response["messages"]:
    m.pretty_print()

# %% [markdown]
# # Exercise 4.9: Compare to trajecotry of LangChain's ReAct implementation: (using `create_agent`)
#

# %%
from langchain.agents import create_agent

langchain_agent = create_agent(model=model, tools=[web_search])
langchain_response = langchain_agent.invoke(HumanMessage(search_query))
