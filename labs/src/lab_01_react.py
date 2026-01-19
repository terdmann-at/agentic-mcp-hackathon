from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate

# Initialize Model
from llm import model as llm

# Tools
search_tool = DuckDuckGoSearchRun()
tools = [search_tool]

# Get ReAct Prompt (or use default)
# We'll stick to a standard one or pull from hub
prompt = hub.pull("hwchase17/react")

# Create Agent
agent = create_react_agent(llm, tools, prompt)

# Create Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def run_react_agent(topic: str):
    """
    Wrapper to run the agent with a single topic string.
    """
    try:
        response = agent_executor.invoke({"input": topic})
        return response["output"]
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test run
    print(run_react_agent("What is the capital of France?"))
