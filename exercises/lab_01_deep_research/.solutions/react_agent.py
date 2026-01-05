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
# Initialize Tools
search_tool = DuckDuckGoSearchRun()
tools = [search_tool]

# Create the Agent (Graph)
# This returns a CompiledGraph
agent = create_react_agent(llm, tools)

def run_react_agent(topic: str) -> str:
    """
    Runs the baseline ReAct agent on a topic.
    """
    print(f"--- Running ReAct Agent on: {topic} ---")
    try:
        # LangGraph agents take 'messages' as input
        messages = [("user", topic)]
        result = agent.invoke({"messages": messages})
        
        # The result 'messages' list contains the conversation history
        # The last message is the AIMessage with the final answer
        final_message = result["messages"][-1]
        return final_message.content
        
    except Exception as e:
        return f"Error: {e}"
# </solution>
