import os
import subprocess
import time
import pytest
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
async def test_deep_agent_snake_game(docker_server):
    """
    Test the Deep Agent's ability to create a multi-file Snake Game.
    Verifies that it can plan the task and use the coding sub-agent to write multiple files.
    """
    
    # Clean sandbox
    if os.path.exists(SANDBOX_ROOT):
        shutil.rmtree(SANDBOX_ROOT)
    os.makedirs(SANDBOX_ROOT, exist_ok=True)

    question = (
        "Develop a simple Snake game using HTML, CSS, and JavaScript. "
        "The project should be multi-file: "
        "1. index.html: The main structure, linking to styles and scripts. "
        "2. style.css: Basic styling for the game board. "
        "3. game.js: The logic of the Snake game. "
        "Use the file system tools to write these files into the sandbox. "
        "Ensure the game is functional and the files are correctly linked."
    )
    print(f"\nQuestion: {question}")

    config = {"recursion_limit": 50, "configurable": {"thread_id": "snake_game_test_thread"}}
    
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

    # Verify Files exist
    index_html = os.path.join(SANDBOX_ROOT, "index.html")
    style_css = os.path.join(SANDBOX_ROOT, "style.css")
    game_js = os.path.join(SANDBOX_ROOT, "game.js")

    assert os.path.exists(index_html), "index.html was not created"
    assert os.path.exists(style_css), "style.css was not created"
    assert os.path.exists(game_js), "game.js was not created"

    # Verify linking in index.html
    with open(index_html, "r") as f:
        content = f.read()
        assert "style.css" in content, "index.html does not link to style.css"
        assert "game.js" in content, "index.html does not link to game.js"

    print("\nSnake Game files successfully created and verified.")

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v", "-s"]))
