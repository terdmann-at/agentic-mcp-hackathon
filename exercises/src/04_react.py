# %% [markdown]
# # Exercise 4: ReAct Agent
#
# In this file, we'll build a ReAct agent using the LangGraph framework.
# It would not be difficult to write an ReAct agent without a framework as well.
# However, LangGraph provides low-level supporting infrastructure for defining agents,
# which makes some things like persistence, state-management easy.
#
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


# %% [markdown]
# ## Tools
#
# Let's define a couple tools.
#


# %%
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
#
# Now we are ready to define the agent. For this we will build a graph,
# consisting of Nodes such as the agent node (where we invoke the LLM), or
# a tool node (where we invoke the tools as requested by the LLM).
#
# Further, we'll define edges (to define the order of execution), and
# conditional edges (branching points), which allows us to create loops.
#
# For the ReAct agent, we'll loop between LLM calls and tool calls. The loop
# ends when the LLM does not emit any tool calls (and thus has provided the final answer).
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
    return str(DDGS().text(query, max_results=max_results))


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
# # Exercise 4.9: Let's use the functional API
#


def build_agent_func(tools):
    # Augment the LLM with tools
    tools_by_name = {tool.name: tool for tool in tools}
    model_with_tools = model.bind_tools(tools)

    from langchain.messages import (
        ToolCall,
    )
    from langchain_core.messages import BaseMessage
    from langgraph.func import entrypoint, task
    from langgraph.graph import add_messages

    # Step 2: Define model node

    @task
    def call_llm(messages: list[BaseMessage]):
        """LLM decides whether to call a tool or not"""
        return model_with_tools.invoke(
            [
                SystemMessage(
                    content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                )
            ]
            + messages
        )

    # Step 3: Define tool node
    @task
    def call_tool(tool_call: ToolCall):
        """Performs the tool call"""
        tool = tools_by_name[tool_call["name"]]
        return tool.invoke(tool_call)

    # Step 4: Define agent
    @entrypoint()
    def agent(messages: list[BaseMessage]):
        model_response = call_llm(messages).result()

        while True:
            if not model_response.tool_calls:
                break

            # Execute tools
            tool_result_futures = [
                call_tool(tool_call) for tool_call in model_response.tool_calls
            ]
            tool_results = [fut.result() for fut in tool_result_futures]
            messages = add_messages(messages, [model_response, *tool_results])
            model_response = call_llm(messages).result()

        messages = add_messages(messages, model_response)
        return messages

    return agent


agent = build_agent_func([add, multiply, divide])
# Invoke
messages = [HumanMessage(content="Add 3 and 4.")]
for chunk in agent.stream(messages, stream_mode="updates"):
    print(chunk)
    print("\n")


# %% [markdown]
# # Exercise 4.10: Try asking what your last query was. How can we get this to work?
# Hint: We need a checkpointer: https://docs.langchain.com/oss/python/langgraph/persistence#checkpoints
#


# %% [markdown]
# # Exercise 4.11 (Bonus): Try out other architetural patterns.
#
#   For example:
#       * add a router
#       * add HITL (explicit confirmation of tool calls)
#       * structured output
