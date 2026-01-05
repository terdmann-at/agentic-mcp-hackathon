# %% [markdown]
# # Exercise 5: Intro to MCP
# 
# Goal: Connect to a standard MCP server (the Filesystem server) and use it to read a directory.
# Prerequisites: You need `npx` installed.


# %%
import asyncio
import os
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

# We will connect to the official MCP filesystem server
# Command: npx -y @modelcontextprotocol/server-filesystem <allowed-path>

SERVER_COMMAND = "npx"
SERVER_ARGS = [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "." # Allow access to current directory
]

async def main():
    # 1. Define Server Params
    server_params = StdioServerParameters(
        command=SERVER_COMMAND,
        args=SERVER_ARGS,
        env=os.environ.copy()
    )

    print("Connecting to MCP Filesystem Server...")

    # 2. Connect
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 3. List Tools
            tools = await session.list_tools()
            print(f"\nConnected! Found {len(tools.tools)} tools:")
            for t in tools.tools:
                print(f" - {t.name}: {t.description[:50]}...")

            # 4. Use a Tool (list_directory)
            print("\nListing directory contents...")
            result = await session.call_tool("list_directory", arguments={"path": "."})
            print(result.content[0].text)

            # 5. Use a Tool (read_file)
            print("\nReading a file...")
            # We assume '01_chatbot.ipynb' exists in this folder
            try:
                read_result = await session.call_tool("read_file", arguments={"path": os.path.abspath("01_chatbot.ipynb")})
                print(f"File content length: {len(read_result.content[0].text)} bytes")
                print("First 100 characters:")
                print(read_result.content[0].text[:100])
            except Exception as e:
                print(f"Error reading file: {e}")

# Run the async main loop
if __name__ == "__main__":
    try:
        # Check if loop is already running (Jupyter)
        loop = asyncio.get_running_loop()
        await main()
    except RuntimeError:
        asyncio.run(main())

