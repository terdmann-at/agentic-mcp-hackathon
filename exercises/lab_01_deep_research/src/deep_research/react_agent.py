from langgraph.prebuilt import create_react_agent
from langchain_openai import AzureChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

# Initialize Model
# We need to ensure the model supports tool calling (Azure OpenAI does)
llm = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)

# Exercise: Build a ReAct Agent
# 1. Initialize the tools (DuckDuckGoSearchRun).
# 2. Create the ReAct agent using `create_react_agent(llm, tools)`.
# 3. Implement `run_react_agent`:
#    - Create a message list: [("user", topic)]
#    - Invoke the agent.
#    - Return the content of the last message in result["messages"].
# <solution>
    # TODO: Implement this
    pass
    # </solution>
