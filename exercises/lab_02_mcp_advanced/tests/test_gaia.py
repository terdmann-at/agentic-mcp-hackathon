import os
import subprocess
import time
import pytest
import os
import shutil
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Import the deep agent graph
from mcp_agent.deep_agent.graph import graph
from mcp_agent.deep_agent.fs_tools import SANDBOX_ROOT

# Load env vars
load_dotenv()

# Configuration
SERVER_SCRIPT = "src/mcp_agent/server/docker_server.py"

@pytest.fixture(scope="module")
def docker_server():
    """Starts the Docker MCP server as a subprocess for the coding sub-agent."""
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
async def test_deep_agent_hard_gaia(docker_server):
    """
    Test the Deep Agent's ability to solve a Hard GAIA Question.
    Requires:
    1. Research (Internet Search) -> Deep Agent
    2. Calculation (Python Execution) -> Delegated to Coding Sub-Agent
    """
    
    # Clean sandbox
    if os.path.exists(SANDBOX_ROOT):
        shutil.rmtree(SANDBOX_ROOT)
    os.makedirs(SANDBOX_ROOT, exist_ok=True)

    # Hard Question
    # Microsoft CEO: Satya Nadella (1967)
    # Sqrt(1967) ≈ 44.35
    # 10th Fibonacci (F1=0, F2=1... F10=34). 
    # Result: 34 * 44.35 = 1507.93
    question = (
        "What is the 10th Fibonacci number (where F1=0, F2=1) multiplied by "
        "the square root of the birth year of the current Microsoft CEO? "
        "Use the 'delegate_code_task' tool to perform the calculation using Python. "
        "Round the final answer to 2 decimal places."
    )
    print(f"\nQuestion: {question}")

    config = {"recursion_limit": 50, "configurable": {"thread_id": "hard_test_thread"}}
    
    final_output = ""
    async for event in graph.astream(
        {"messages": [HumanMessage(content=question)]},
        config=config,
        stream_mode="updates"
    ):
        for node, values in event.items():
            print(f"Node: {node}")
            if "messages" in values:
                last_msg = values["messages"][-1]
                print(f"Message: {last_msg}")
                if hasattr(last_msg, "content"):
                    final_output = last_msg.content

    print(f"\nFinal Output: {final_output}")

    # Verify Logic
    assert "1507.93" in final_output, "Final output did not contain the correct calculated value (approx 1507.93)"
    assert "Satya Nadella" in final_output, "Did not identify Microsoft CEO."

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v", "-s"]))
