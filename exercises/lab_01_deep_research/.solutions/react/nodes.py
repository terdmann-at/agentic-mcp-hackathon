from langchain_openai import AzureChatOpenAI
from deep_research.react.state import AgentState
from deep_research.react.tools import tools
from langgraph.prebuilt import ToolNode

# Initialize Model with Tools
llm = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
llm_with_tools = llm.bind_tools(tools)


# Exercise: Implement call_model
# 1. Inspect the state to get messages.
# 2. Invoke 'llm_with_tools' with these messages.
# 3. Return the response in a dictionary under key "messages" (wrapped in a list).
# <solution>
def call_model(state: AgentState):
    """
    Invokes the model with the current state messages.
    """
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# </solution>

# We can use the prebuilt ToolNode for simplicity in execution,
# or implement it manually as an advanced exercise.
# For now, let's use the prebuilt one to focus on the Graph structure.
tool_node = ToolNode(tools)


# Exercise: Implement should_continue
# Checks the last message in the state.
# If it has 'tool_calls', return "tools".
# Otherwise, return "__end__".
# <solution>
def should_continue(state: AgentState):
    """
    Conditional logic:
    - If the last message has tool_calls, go to 'tools'.
    - Otherwise, go to END.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"


# </solution>
