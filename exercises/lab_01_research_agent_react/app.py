import streamlit as st
from databricks_langchain import ChatDatabricks
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# --- Initial Setup ---
st.set_page_config(layout="wide")

# Setup LLM and Tools
try:
    # Use the model from the initial setup
    llm = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5")
except Exception as e:
    st.error(f"Failed to initialize ChatDatabricks: {e}")
    st.stop()

# Initialize Search Tool
try:
    search_tool = DuckDuckGoSearchRun()
    tools = [search_tool]
except Exception as e:
    st.warning(f"Failed to initialize search tool: {e}. Search functionality may not work.")
    search_tool = None 
    tools = []

# Bind tools to LLM
if tools:
    llm_with_tools = llm.bind_tools(tools)
else:
    llm_with_tools = llm

# --- State Definitions ---

class AgentState(TypedDict):
    """
    The state of our ReAct agent.
    It simply holds a list of messages.
    """
    messages: Annotated[list[BaseMessage], add_messages]

# --- Nodes ---

def call_model(state: AgentState):
    """
    Invokes the model with the current state messages.
    """
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

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

# We use the prebuilt ToolNode for simplicity
tool_node = ToolNode(tools)

# --- Graph Definition ---

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
react_app = workflow.compile()

# --- Application UI ---

st.title("🤖 ReAct Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    # Filter out non-displayable messages if necessary, or just display user/assistant ones
    if isinstance(message, dict):
        role = message.get("role")
        content = message.get("content")
    else:
        # Handle BaseMessage objects if they end up in history (though we usually append dicts for UI)
        role = message.type
        content = message.content
        
    if role in ["user", "assistant"]:
         with st.chat_message(role):
            st.markdown(content)

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Invoke the graph
                # LangGraph agents take 'messages' as input
                initial_inputs = {"messages": [("user", prompt)]}
                
                # We can verify it works by streaming or just invoking
                result = react_app.invoke(initial_inputs)

                # The result 'messages' list contains the conversation history
                # The last message is the AIMessage with the final answer
                final_message = result["messages"][-1]
                response_content = final_message.content

                st.markdown(response_content)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_content}
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
