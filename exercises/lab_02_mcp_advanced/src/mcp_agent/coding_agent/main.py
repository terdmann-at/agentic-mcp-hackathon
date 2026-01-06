import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import AzureChatOpenAI
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import StdioServerParameters, stdio_client

# Local imports
from mcp_agent.tools.web_search import web_search

from .agent import build_agent

# Configuration

DOCKER_SERVER_SCRIPT = "src/mcp_agent/server/docker_server.py"


async def amain():
    load_dotenv()
    # 1. Server Parameters

    # Docker MCP Server (Remote SSE)
    # Ensure you run `uv run src/mcp_agent/server/docker_server.py` in a separate terminal!
    docker_server_url = "http://localhost:8000/sse"

    # Sequential Reasoning MCP Server (Remote/Node)
    reasoning_server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
        env=os.environ.copy(),
    )

    print("Connecting to MCP servers...")

    # 2. Connect to both servers
    # We use sse_client for Docker and stdio_client for Reasoning
    async with (
        sse_client(docker_server_url) as (read_docker, write_docker),
        stdio_client(reasoning_server_params) as (read_reasoning, write_reasoning),
    ):
        async with (
            ClientSession(read_docker, write_docker) as session_docker,
            ClientSession(read_reasoning, write_reasoning) as session_reasoning,
        ):
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
            model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
            agent = build_agent(model, all_tools)

            # 5. Run the Agent
            print("\n" + "=" * 50)
            print("Advanced Agent Ready. Enter your query (or 'q' to quit).")
            print("=" * 50 + "\n")

            while True:
                user_input = input("User: ")
                if user_input.lower() in ["q", "quit", "exit"]:
                    break

                async for chunk in agent.astream(
                    {"messages": [HumanMessage(content=user_input)]},
                    stream_mode="values",
                ):
                    if chunk["messages"]:
                        last_msg = chunk["messages"][-1]
                        last_msg.pretty_print()


def main():
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
