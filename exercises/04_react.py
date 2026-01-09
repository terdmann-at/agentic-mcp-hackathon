# %% [markdown]
# # Exercise 4: ReAct Agent
#
# Goal: Build a ReAct agent from scratch using LangGraph.
#
# To test your solution, run:
#
#       uv run 04_react.py
#

# %%
import operator
from typing import Literal

from dotenv.main import load_dotenv
from langchain.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict

load_dotenv()

model = AzureChatOpenAI(
    temperature=1,
    deployment_name="gpt-4.1",
)


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

# Exercise 4.2: Create a search tool
# Hint: Initialize DuckDuckGoSearchRun()
# <solution>
search_tool = DuckDuckGoSearchRun()
# </solution>

tools = [add, multiply, divide, search_tool]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)


# %%
# State
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


# %%
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
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
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
def main():
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

    # Exercise 4.6: Compile the graph
    # Hint: Call .compile() on the graph builder.
    # <solution>
    agent = agent_builder.compile()
    # </solution>

    # Run
    print("--- Math Problem ---")
    math_query = "Calculate ((144 / 12) * (25 + 75)) / ((10 * 10) / (500 / 5)) + ((81 / 9) * (121 / 11))"
    messages = [HumanMessage(content=math_query)]

    # Exercise 4.7: Invoke the agent
    # Hint: Use agent.invoke({"messages": messages})
    # <solution>
    math_messages = agent.invoke({"messages": messages})
    # </solution>

    for m in math_messages["messages"]:
        m.pretty_print()

    print("\n--- Search Problem ---")
    search_query = "Who won the Super Bowl in 2024?"
    messages = [HumanMessage(content=search_query)]
    search_messages = agent.invoke({"messages": messages})
    
    for m in search_messages["messages"]:
        m.pretty_print()


if __name__ == "__main__":
    main()
