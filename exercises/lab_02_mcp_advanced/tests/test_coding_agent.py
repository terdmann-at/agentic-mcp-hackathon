import pytest
import subprocess
import time
import os
import sys
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Import the agent builder
from mcp_agent.coding_agent.agent import build_agent
from mcp_agent.tools.web_search import web_search

# Load env vars
load_dotenv()

# Configuration
SERVER_SCRIPT = "src/mcp_agent/server/docker_server.py"
PORT = 8000
SSE_URL = f"http://localhost:{PORT}/sse"

@pytest.fixture(scope="module")
def docker_server():
    """Starts the Docker MCP server as a subprocess."""
    print("Starting Docker MCP Server...")
    process = subprocess.Popen(
        ["uv", "run", SERVER_SCRIPT],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    
    # Wait for server to start
    started = False
    start_time = time.time()
    while time.time() - start_time < 20:
        if process.poll() is not None:
            raise RuntimeError(
                f"Server failed to start. Return code: {process.returncode}"
            )
        time.sleep(1)
        # Assuming it takes ~5s
        if time.time() - start_time > 5:
            started = True
            break

    if not started and process.poll() is not None:
        stdout, stderr = process.communicate()
        raise RuntimeError(f"Server exited early:\nSTDOUT: {stdout}\nSTDERR: {stderr}")

    print("Docker Server likely started (5s wait).")
    yield process

    print("\nStopping Docker MCP Server...")
    process.terminate()
    process.wait()

@pytest.mark.asyncio
async def test_coding_agent_plot_titanic(docker_server):
    """
    Test the Coding Agent's ability to use the Docker environment to:
    1. Load a CSV file (titanic.csv)
    2. Create a plot (Age distribution)
    3. Save the plot to a file
    """
    
    # 1. Connect and Setup
    reasoning_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
        env=os.environ.copy(),
    )

    print("Connecting to clients...")
    async with (
        sse_client(SSE_URL) as (read_docker, write_docker),
        stdio_client(reasoning_params) as (read_reasoning, write_reasoning),
    ):
        async with (
            ClientSession(read_docker, write_docker) as session_docker,
            ClientSession(read_reasoning, write_reasoning) as session_reasoning,
        ):
            await session_docker.initialize()
            await session_reasoning.initialize()

            docker_tools = await load_mcp_tools(session_docker)
            reasoning_tools = await load_mcp_tools(session_reasoning)
            local_tools = [web_search]

            all_tools = docker_tools + reasoning_tools + local_tools
            
            print(f"Loaded tools: {[t.name for t in all_tools]}")

            model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
            agent = build_agent(model, all_tools)

            # 2. Plotting Task
            # titanic.csv is mounted in /data/titanic.csv inside the container
            question = (
                "I have a dataset at '/data/titanic.csv'. "
                "Please load it using pandas, create a histogram of the 'Age' distribution, "
                "and save the plot as '/data/age_distribution.png'. "
                "Verify the file exists after creating it."
            )
            print(f"\nQuestion: {question}")

            final_answer = ""
            async for chunk in agent.astream(
                {"messages": [HumanMessage(content=question)]}, stream_mode="values"
            ):
                if chunk["messages"]:
                    msg = chunk["messages"][-1]
                    final_answer = msg.content

            print(f"\nFinal Answer: {final_answer}")

            # 3. Verification
            # We can verify by asking the agent to check if the file exists using python
            # Or we can check the final answer. 
            # A robust check is to use the docker tool directly to check file existence.
            
            # For simplicity, we'll verify via the agent's output and a direct check command
            check_code = "import os; print(os.path.exists('/data/age_distribution.png'))"
            api_result = await session_docker.call_tool("execute_python", arguments={"code": check_code})
            
            print(f"Verification Result: {api_result.content}")
            assert "True" in str(api_result.content), "The plot file 'age_distribution.png' was not created."

if __name__ == "__main__":
    # Allow running directly
    sys.exit(pytest.main([__file__, "-v", "-s"]))
