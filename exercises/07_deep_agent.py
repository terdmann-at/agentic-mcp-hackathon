# %% [markdown]
# # Exercise 7: Deep Agents (FileSystem Memory)
#
# Goal: Build a "Deep Agent" that uses the local filesystem to manage context and memory.
#
# "Deep Agents" in LangChain often refer to agents that can handle long-running tasks by persistenting state, plans, and research notes to files, rather than keeping everything in the context window.
#
# Prerequisites: `uv add langchain-community` (if not already present)

# %%
import tempfile
from pathlib import Path

# We'll work in a temporary directory for safety
working_dir = Path(tempfile.mkdtemp())
print(f"Working in: {working_dir}")

# %%
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_openai import AzureChatOpenAI

# 1. Setup Tools
# The FileManagementToolkit gives the agent tools like:
# read_file, write_file, list_directory, file_exists, etc.
toolkit = FileManagementToolkit(root_dir=str(working_dir))
tools = toolkit.get_tools()

print(f"Tools available: {[t.name for t in tools]}")

# 2. Setup Model
model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)

# 3. Setup Agent
# We use a standard ReAct prompt
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# %%
# 4. Run the Agent
# We ask the agent to perform a multi-step task that benefits from "writing things down"

task = """
I want you to research the following topic: "The history of the Python programming language".
Since you cannot browse the web, just use your internal knowledge.

Please follow this process:
1. Create a plan and save it to "plan.txt".
2. Write a brief history of Python (1 paragraph) and save it to "history.txt".
3. Write a list of key versions (e.g. 1.0, 2.0, 3.0) and save it to "versions.txt".
4. Finally, read "plan.txt" to check if you missed anything, and if done, tell me "Mission Accomplished".
"""

agent_executor.invoke({"input": task})

# %%
# 5. Verify Output
# Let's inspect the files the agent created
print("\n--- Listing Files ---")
import os

for root, dirs, files in os.walk(working_dir):
    for file in files:
        print(f"File: {file}")
        content = (working_dir / file).read_text()
        print(f"Content:\n{content}\n")

# %% [markdown]
# ### Takeaway
# By giving the agent `write_file` and `read_file` capabilities, we allow it to:
# 1. **Offload Memory**: It doesn't need to remember the full history in its context window.
# 2. **Persist State**: If the agent crashes or pauses, the files remain.
# 3. **Share Context**: Other agents could read these files to pick up where this one left off.
