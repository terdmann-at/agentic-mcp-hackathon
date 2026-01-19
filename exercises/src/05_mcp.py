# %% [markdown]
# # Exercise 5: Intro to MCP
#
# In this notebook, we'll define a MCP server and deploy it via Databricks Apps.
#
# Then, we will connect to it via a client.
#

# %%
# %mkdir custom_mcp_server

# %%
# %%writefile custom_mcp_server/app.py
from fastmcp import FastMCP

mcp = FastMCP(name="MyServer")


@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)


# %% [markdown]
#
# For the Databricks Apps deployment, we'll need two extra files:
#
# %%
with open("custom_mcp_server/app.yaml", "w") as f:
    f.write("command: ['python', 'main.py']")

with open("custom_mcp_server/requirements.txt", "w") as f:
    f.write("fastmcp")

# %% [markdown]
# # Deployment
#
# Head to "Compute" -> "Apps" -> "Create Custom App"
#
# Now let's define an agent that will use the tools from the MCP server.
#

# %% [markdown]
#
# Now let's define an agent that will use the tools from the MCP server.
#
# First we will need some packages again.
#
# %%
# %pip install langchain langgraph databricks-langchain
# %restart_python

# %%
import asyncio
from typing import Annotated, Any, Optional, Sequence, TypedDict, Union

import nest_asyncio
from databricks.sdk import WorkspaceClient
from databricks_langchain import (
    DatabricksMCPServer,
    DatabricksMultiServerMCPClient,
)
from langchain.messages import AIMessage, AnyMessage
from langchain_core.language_models import LanguageModelLike
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain_core.tools import BaseTool
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode

# %%
#
# In order to connect to the MCP server in the Databricks Apps application, we
# need to create a service principal. Upon creating we get the client id and secret,
# which we will use below.
#
# The host is just the url you are at currently.
#
# This client requires OAuth with a service principal for machine-to-machine (M2M) auth.
# Follow the insturctions here in order to create a SP, grant the SP query permissions on your app and then mint a client id and secret.
# https://docs.databricks.com/aws/en/dev-tools/auth/oauth-m2m

custom_mcp_server_workspace_client = WorkspaceClient(
    host="<workspace-url>",
    client_id="<client-id>",
    client_secret="<client-secret>"
    auth_type="oauth-m2m",  # Enables service principal authentication
)

#
# Exercise 5.1: Configure the MCP Client with the server details
# You need to fill in the `name` and `url` for the DatabricksMCPServer.
# For this exercise, assume we have a server named "MyServer" running at the provided URL.
databricks_mcp_client = DatabricksMultiServerMCPClient(
    [
        # DatabricksMCPServer(
        #     name="system-ai",
        #     url=f"{host}/api/2.0/mcp/functions/system/ai",
        # ),
        DatabricksMCPServer(
            # <solution>
            name="MyServer",
            url="http://0.0.0.0:8000/sse",
            workspace_client=custom_mcp_server_workspace_client,
            # </solution>
        ),
    ]
)

# %% [markdown]
#
# Now let's connect the client to an Agent.
#

# %%
nest_asyncio.apply()
from llm import model as llm

system_prompt = """
You are a helpful assistant that can run Python code.
"""


# The state for the agent workflow, including the conversation and any custom data
class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_messages]
    custom_inputs: Optional[dict[str, Any]]
    custom_outputs: Optional[dict[str, Any]]


def create_tool_calling_agent(
    model: LanguageModelLike,
    tools: Union[ToolNode, Sequence[BaseTool]],
    system_prompt: Optional[str] = None,
):
    model = model.bind_tools(tools)  # Bind tools to the model

    # Function to check if agent should continue or finish based on last message
    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        # If function (tool) calls are present, continue; otherwise, end
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "continue"
        else:
            return "end"

    def clean_content(messages):
        for m in messages:
            if hasattr(m, "content") and isinstance(m.content, list):
                for block in m.content:
                    if isinstance(block, dict):
                        block.pop("id", None)  # Remove the offending field
        return messages

    # Preprocess: optionally prepend a system prompt to the conversation history
    if system_prompt:
        preprocessor = RunnableLambda(
            lambda state: [{"role": "system", "content": system_prompt}]
            + clean_content(state["messages"])
        )
    else:
        preprocessor = RunnableLambda(lambda state: clean_content(state["messages"]))

    model_runnable = preprocessor | model  # Chain the preprocessor and the model

    # The function to invoke the model within the workflow
    def call_model(
        state: AgentState,
        config: RunnableConfig,
    ):
        response = model_runnable.invoke(state, config)
        return {"messages": [response]}

    workflow = StateGraph(AgentState)  # Create the agent's state machine

    workflow.add_node("agent", RunnableLambda(call_model))  # Agent node (LLM)
    workflow.add_node("tools", ToolNode(tools))  # Tools node

    workflow.set_entry_point("agent")  # Start at agent node
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",  # If the model requests a tool call, move to tools node
            "end": END,  # Otherwise, end the workflow
        },
    )
    workflow.add_edge("tools", "agent")  # After tools are called, return to agent node

    # Compile and return the tool-calling agent workflow
    return workflow.compile()


# Initialize the entire agent, including MCP tools and workflow
def initialize_agent():
    """Initialize the agent with MCP tools"""
    # Create MCP tools from the configured servers
    mcp_tools = asyncio.run(databricks_mcp_client.get_tools())
    print(mcp_tools)
    # Create the agent graph with an LLM, tool set, and system prompt (if given)
    agent = create_tool_calling_agent(llm, mcp_tools, system_prompt)
    return agent


# %%
agent = initialize_agent()
agent.invoke({"messages:"["what tools you have?"]})
