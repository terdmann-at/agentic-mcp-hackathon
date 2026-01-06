# %% [markdown]
# # Exercise 4: ReAct Agent
#
# Goal: Build a ReAct agent from scratch using LangGraph.


# %%
import operator
from typing import Literal

from langchain.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict

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


@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.Args: a: First int, b: Second int"""
    return a / b


tools = [add, multiply, divide]
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


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tool_node"
    return END


# %%
# Build Graph
agent_builder = StateGraph(MessagesState)
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
agent_builder.add_edge("tool_node", "llm_call")

agent = agent_builder.compile()


# %%
# Run
user_query = "Calculate ((144 / 12) * (25 + 75)) / ((10 * 10) / (500 / 5)) + ((81 / 9) * (121 / 11))"
messages = [HumanMessage(content=user_query)]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()
