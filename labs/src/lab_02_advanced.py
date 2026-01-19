# %% [markdown]
# # Lab 2: Multi-Agent System (MAS) with Progressive Disclosure
#
# In this lab, we build a Supervisor/Router agent that manages specialized sub-agents.
#
# The Main Agent does NOT see all tools at once (which can start overwhelm the context if we were to keep adding tools).
# Instead, it has two meta-tools:
# 1. `search_tools(query)`: Finds relevant specialized agents.
# 2. `call_tool(name, task)`: Delegates the task to a specific agent.
#
# **Sub-Agents**:
# 1. **Searcher**: A ReAct agent with web search capabilities (from Exercise 4).
# 2. **Coder**: A Code Execution agent (from Exercise 6).
#
# Finally, we evaluate this system against the GAIA benchmark.

# %%
# %pip install langchain langgraph ddgs databricks-langchain smolagents pandas
# %restart_python

# %%
import re

import pandas as pd
from ddgs import DDGS
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool

# Initialize generic model
from llm import model as llm
from smolagents import LocalPythonExecutor

# %% [markdown]
# ## 1. Define Sub-Agents (The Specialists)
#
# These are "factories" that create a fresh agent instance when called.
# This ensures isolation of state between calls.


# %%
@tool
def web_search(query: str, max_results: int = 5):
    """Run a web search"""
    return str(DDGS().text(query, max_results=max_results))


def make_search_agent():
    """Creates a ReAct agent equipped with Web Search."""
    # Exercise 2.1: Create a ReAct agent using `create_agent`
    # Hint: pass the llm and the list of tools ([web_search])
    # <solution>
    return create_agent(llm, tools=[web_search])
    # </solution>


@tool
def exec_python(code: str):
    """
    Evaluate python code.
    """
    # Initialize a fresh executor for safety/isolation per call if needed,
    # but here we use a shared one for the session or per-turn.
    # For a true tool usage, we might want a new interpreter each time or keep state.
    # Let's create a fresh one to be safe.
    interpreter = LocalPythonExecutor(
        additional_authorized_imports=[
            "pandas",
            "matplotlib",
            "sklearn",
            "numpy",
            "datetime",
        ],
    )
    # We can inject some default data if needed, but we'll start empty.
    try:
        output = interpreter(code)
        return f"Stdout:\n{str(interpreter.state['_print_outputs'])}\nOutput: {output}"
    except Exception as e:
        return f"Execution Error: {e}"


def make_coding_agent():
    """Creates a generic agent equipped with a Python Code Executor."""
    # Exercise 2.2: Create a coding agent
    # Hint: Use `create_agent` with [exec_python] tool
    # <solution>
    return create_agent(llm, tools=[exec_python])
    # </solution>


# %% [markdown]
# ## 2. Tool Registry & Discovery Mechanism
#
# We define the "Registry" of available skills.

# %%
TOOL_REGISTRY = {
    "SearchAgent": {
        "description": "Capable of searching the live internet for up-to-date facts, news, and general knowledge.",
        "factory": make_search_agent,
    },
    "CodingAgent": {
        "description": "Capable of writing and executing Python code to solve math problems, data analysis, or algorithmic tasks.",
        "factory": make_coding_agent,
    },
}


@tool
def search_tools(query: str) -> str:
    """
    Search for available tools/agents relevant to the query.
    Returns a list of tool names and their descriptions.
    """
    print(f"--- [Main] Searching tools for: {query} ---")
    results = []
    # Exercise 2.3: Implement Tool Discovery
    # Iterate over TOOL_REGISTRY and format the name and description for the LLM.
    # <solution>
    for name, info in TOOL_REGISTRY.items():
        results.append(f"- Tool: {name}\n  Description: {info['description']}")
    # </solution>
    return "\n".join(results)


@tool
def call_tool(tool_name: str, task: str) -> str:
    """
    Delegates a specific task to a named tool/agent.
    """
    print(f"--- [Main] Calling {tool_name} with task: {task[:50]}... ---")

    entry = TOOL_REGISTRY.get(tool_name)
    if not entry:
        return f"Error: Tool '{tool_name}' not found. Please use 'search_tools' to see available tools."

    # Exercise 2.4: Implement Tool Delegation
    # 1. Instantiate the agent using the factory
    # 2. Invoke the agent with the task (wrapped in HumanMessage)
    # 3. Return the content of the last message
    # <solution>
    # 1. Instantiate the agent (Just-In-Time)
    agent_app = entry["factory"]()

    # 2. Invoke the agent
    # The sub-agent expects a list of messages.
    try:
        result = agent_app.invoke({"messages": [HumanMessage(content=task)]})
        # 3. Extract final response
        last_msg = result["messages"][-1]
        return last_msg.content
    except Exception as e:
        return f"Error executing {tool_name}: {e}"
    # </solution>


# %% [markdown]
# ## 3. Main Agent (The Supervisor)
#
# The Main Agent only has access to `search_tools` and `call_tool`.


# %%
def make_main_agent():
    system_prompt = (
        "You are a helpful Assistant and Project Manager. "
        "You do not have direct abilities to search or code. "
        "Instead, you must:"
        "\n1. Analyze the user's request."
        "\n2. Use 'search_tools' to find capable sub-agents."
        "\n3. Use 'call_tool' to delegate work to them."
        "\n4. Synthesize their outputs into a final answer."
        "\n\nAlways verify which tool matches the needs before calling it."
    )

    # Exercise 2.5: Create the Main Agent
    # Give it access to `search_tools` and `call_tool`.
    # <solution>
    return create_agent(
        llm, tools=[search_tools, call_tool], system_prompt=system_prompt
    )
    # </solution>


main_agent = make_main_agent()

# %% [markdown]
# ## 4. Evaluation Loop (GAIA Benchmark)
#
# We evaluate the system on the GAIA validation set.


# %%
def run_gaia_eval():
    csv_path = "gaia_validation_level1.csv"  # Ensure this file exists in CWD
    try:
        # Load first 2 examples for quick testing
        df = pd.read_csv(csv_path)[:2]
        print(f"Loaded {len(df)} tasks for evaluation.")
    except FileNotFoundError:
        print(f"Dataset not found at {csv_path}. Please generate it first.")
        return

    results = []

    # Simple Judge Logic (Internal function to avoid external dependency for now)
    def query_judge(question, predicted, truth):
        prompt = f"""
        [QUESTION]: {question}
        [GROUND TRUTH]: {truth}
        [PREDICTED]: {predicted}

        Compare Predicted to Ground Truth. Score 1 (Wrong) to 10 (Perfect).
        Format: SCORE: <int>
        """
        try:
            res = llm.invoke(prompt).content
            match = re.search(r"SCORE:\s*(\d+)", res)
            return int(match.group(1)) if match else 0
        except:
            return 0

    for idx, row in df.iterrows():
        question = row["Question"]
        truth = row["Final answer"]

        print(f"\nProcessing Task {idx + 1}: {question}")

        # Exercise 2.6: Invoke the Main Agent
        # Invoke `main_agent` with the question and get the final response.
        # <solution>
        try:
            response = main_agent.invoke({"messages": [HumanMessage(content=question)]})
            predicted = response["messages"][-1].content
        except Exception as e:
            predicted = f"Error: {e}"
        # </solution>

        print(f"[Result]: {predicted[:100]}...")

        score = query_judge(question, predicted, truth)
        print(f"[Score]: {score}")

        results.append(
            {
                "question": question,
                "truth": truth,
                "predicted": predicted,
                "score": score,
            }
        )

    print("\n=== Final Results ===")
    print(pd.DataFrame(results))


# %%
# Try the system out
question = (
    "What is the 10th Fibonacci number (where F1=0, F2=1) multiplied by "
    "the square root of the birth year of the current Microsoft CEO? "
    "Delegate web search and coding tasks using appropriate tools. "
    "Round the final answer to 2 decimal places."
)
res = main_agent.invoke({"messages": [HumanMessage(question)]})
print(f"Agent: {res['messages'][-1].content}")


# %%
# Exercise 2.7 (Bonus): Try to optimize the agent to do well on the eval.
# run_gaia_eval()
