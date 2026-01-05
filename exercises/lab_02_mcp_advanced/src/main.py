
import asyncio
import os
import sys
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import create_react_agent
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools

# Local tools
from src.tools.web_search import visit_webpage
from langchain_core.tools import tool

@tool
def web_search(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string."""
    return visit_webpage(url)

# Configuration
DOCKER_SERVER_SCRIPT = "src/mcp_server_docker.py"
# We assume the user has `uv` installed to run the local python server, 
# and `npx` to run the sequential reasoning server.

async def main():
    # 1. Server Parameters
    
    # Docker MCP Server (Local Python)
    docker_server_params = StdioServerParameters(
        command="uv",
        args=["run", DOCKER_SERVER_SCRIPT],
        env=os.environ.copy(),
    )

    # Sequential Reasoning MCP Server (Remote/Node)
    # npx -y @modelcontextprotocol/server-sequential-thinking
    reasoning_server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
        env=os.environ.copy(),
    )

    print("Connecting to MCP servers...")
    
    # 2. Connect to both servers
    # We nest the context managers to have both sessions active
    async with stdio_client(docker_server_params) as (read_docker, write_docker), \
               stdio_client(reasoning_server_params) as (read_reasoning, write_reasoning):
        
        async with ClientSession(read_docker, write_docker) as session_docker, \
                   ClientSession(read_reasoning, write_reasoning) as session_reasoning:
            
            await session_docker.initialize()
            await session_reasoning.initialize()
            
            print("Connected to Docker and Reasoning servers.")

            # 3. Load Tools
            docker_tools = await load_mcp_tools(session_docker)
            reasoning_tools = await load_mcp_tools(session_reasoning)
            local_tools = [web_search]
            
            all_tools = docker_tools + reasoning_tools + local_tools
            
            tool_names = [t.name for t in all_tools]
            print(f"Loaded tools: {tool_names}")

            # 4. Create the Agent
            model = AzureChatOpenAI(deployment_name="gpt-4o", temperature=0)
            
            # Simple ReAct agent with all tools available
            # For a true multi-agent system, we would split these tools across different nodes
            # but for this lab starter, a single powerful agent is a good first step,
            # or we can verify the 'Supervisor' pattern if desired.
            # Let's start with a ReAct agent that has Access to EVERYTHING.
            
            system_message = """You are an advanced autonomous research assistance.
            You have access to the following capabilities:
            1. **Sequential Thinking**: Use this to plan your approach and breakdown complex problems. 
               ALWAYS start by using this tool to plan your steps.
            2. **Docker Code Execution**: You can execute Python code in a safe sandboxed environment. 
               Use this for calculations, data analysis, or verifying code logic. 
               The environment has pandas and matplotlib installed.
            3. **Web Search**: You can visit webpages to gather information.
            
            Solve the user's request by combining these tools. 
            """
            
            agent = create_react_agent(model, all_tools, state_modifier=system_message)

            # 5. Run the Agent
            print("\n" + "="*50)
            print("Advanced Agent Ready. Enter your query (or 'q' to quit).")
            print("="*50 + "\n")
            
            while True:
                user_input = input("User: ")
                if user_input.lower() in ["q", "quit", "exit"]:
                    break
                
                async for chunk in agent.astream(
                    {"messages": [HumanMessage(content=user_input)]}, 
                    stream_mode="values"
                ):
                    if chunk["messages"]:
                        last_msg = chunk["messages"][-1]
                        last_msg.pretty_print()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
