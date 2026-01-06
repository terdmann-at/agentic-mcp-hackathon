from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

# Import tools that sub-agents might need
from mcp_agent.tools.web_search import web_search

from .coding_subagent import delegate_code_task
from .fs_tools import fs_tools


@tool
def research_task(
    instructions: str,
    # In a real dynamic system, we might allow choosing tools.
    # For now, we give sub-agents a standard set of tools.
) -> str:
    """Delegate a Research or Filesystem task to a standard sub-agent.

    The sub-agent has access to web search and the filesystem.
    It operates in an isolated context.

    Args:
        instructions: Detailed instructions for the sub-agent.
    """

    # 1. Initialize the model (using same config as main agent)
    model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)

    # 2. Define tools for the sub-agent
    # Sub-agents get search and filesystem access
    sub_tools = [web_search] + fs_tools

    # 3. Create the agent
    sub_agent = create_react_agent(model, sub_tools)

    # 4. Run the agent
    input_message = HumanMessage(content=instructions)

    try:
        # We invoke the agent and get the final state
        result = sub_agent.invoke(
            {"messages": [input_message]},
            config={"recursion_limit": 20},  # Limit steps
        )

        # Extract the last message content
        last_message = result["messages"][-1]
        return f"Sub-agent completed task.\nResult:\n{last_message.content}"

    except Exception as e:
        return f"Sub-agent failed: {str(e)}"


subagent_tools = [research_task, delegate_code_task]
