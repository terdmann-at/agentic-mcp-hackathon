import os
import sys
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

from mcp_agent.coding_agent.agent import build_agent
from mcp_agent.tools.web_search import web_search

# Configuration for Docker MCP Server (Assumes it's running via fixture or manually)
PORT = 8000
SSE_URL = f"http://localhost:{PORT}/sse"

@tool
async def delegate_code_task(instructions: str) -> str:
    """
    Delegates a coding or data analysis task to a specialized Coding Agent.
    
    The Coding Agent has access to:
    1. A Python environment (via Docker) with pandas and matplotlib.
    2. A filesystem for reading/writing data.
    3. Web search.
    
    Use this tool when you need to:
    - Execute Python code.
    - Analyze datasets (e.g., CSV files).
    - Generate plots or visualizations.
    - Perform complex calculations.
    
    Args:
        instructions: Detailed natural language instructions for the coding task.
                     Include file paths if relevant (data is at /data/).
    """
    print(f"\n[Coding SubAgent] Received task: {instructions[:100]}...")
    
    # <solution>
    # 1. Setup Connection to Reasoning Server (stdio)
    # We need to construct the environment for the node process
    env = os.environ.copy()
    reasoning_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
        env=env,
    )

    try:
        # 2. Establish Connections
        # Note: We create a fresh session for isolation. 
        # In a production app, we might pool these or pass a shared session.
        async with (
            sse_client(SSE_URL) as (read_docker, write_docker),
            stdio_client(reasoning_params) as (read_reasoning, write_reasoning),
        ):
            async with (
                ClientSession(read_docker, write_docker) as session_docker,
                ClientSession(read_reasoning, write_reasoning) as session_reasoning,
            ):
                # 3. Initialize Sessions
                await session_docker.initialize()
                await session_reasoning.initialize()

                # 4. Load Tools
                docker_tools = await load_mcp_tools(session_docker)
                reasoning_tools = await load_mcp_tools(session_reasoning)
                local_tools = [web_search]

                all_tools = docker_tools + reasoning_tools + local_tools
                
                # 5. Build Agent
                model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
                agent = build_agent(model, all_tools)
                
                # 6. Run Agent
                # We'll stream output to show progress in stdout, but capture final answer
                final_answer = "No answer produced."
                
                print("[Coding SubAgent] Running...")
                async for chunk in agent.astream(
                    {"messages": [HumanMessage(content=instructions)]},
                    stream_mode="values"
                ):
                    if chunk["messages"]:
                        last_msg = chunk["messages"][-1]
                        if last_msg.type == "ai":
                            final_answer = last_msg.content
                            # print(f"  [SubAgent Partial]: {final_answer[:50]}...")

                print("[Coding SubAgent] Completed.")
                return f"Coding Agent Task Completed.\n\nResult:\n{final_answer}"

    except Exception as e:
        error_msg = f"Coding SubAgent Failed: {str(e)}"
        print(f"[Coding SubAgent] Error: {error_msg}")
        return error_msg
    # </solution>
