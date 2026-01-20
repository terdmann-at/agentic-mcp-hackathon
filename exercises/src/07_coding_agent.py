# %% [markdown]
# # Exercise 7: Coding Agent - "Plan in Code"
#
# In this exercise, we implement an agent that performs "Deep Research" by generating and executing Python code.
# Instead of standard tool calling (JSON), the agent writes a Python script that orchestrates tool usage.
#
# This pattern allows for complex logic, loops, and variable handling directly in the plan.
#
# We will inject two custom tools into the Python execution environment:
# 1. `search(query)`: Performs a web search.
# 2. `synthesize(data)`: Uses the LLM to summarize/synthesize findings.

# %%
# %pip install langchain smolagents databricks-langchain ddgs langchain-community
# %restart_python

# %%

from ddgs import DDGS
from langchain.messages import HumanMessage, SystemMessage

# Initialize Model
from llm import model as llm
from smolagents import LocalPythonExecutor

# %% [markdown]
# ## 1. Define Tools as Python Functions
#
# These functions will be "exposed" to the `LocalPythonExecutor`.


# %%
def search(query: str) -> str:
    """
    Searches the web for the given query.
    Returns the search results as a string.
    """
    print(f"--> [Tool: Search] '{query}'")
    try:
        results = DDGS().text(query, max_results=3)
        return str(results)
    except Exception as e:
        return f"Search Error: {e}"


# Exercise 7.1: Define the `synthesize` tool
# This tool should take a string (content) and use the LLM to summarize/synthesize it.
# We want the agent to use this to process search results.
# Hint: Use `llm.invoke` with a prompt.
# <solution>
def synthesize(content: str) -> str:
    """
    Synthesizes/Summarizes the provided content using an LLM.
    """
    print(f"--> [Tool: Synthesize] Processing {len(content)} chars...")
    prompt = f"Summarize and synthesize the following information:\n\n{content}"
    response = llm.invoke(prompt)
    return response.content


# </solution>


# %% [markdown]
# ## 2. Setup Code Executor
#
# We configure `LocalPythonExecutor` and inject our tools.

# %%
# Exercise 7.2: Initialize LocalPythonExecutor
# Inject `search` and `synthesize` into the environment.
# Hint: Inject tools into `interpreter.state`.
# <solution>
interpreter = LocalPythonExecutor(additional_authorized_imports=["datetime", "math"])
# Inject our custom functions into the global scope of the interpreter
interpreter.state["search"] = search
interpreter.state["synthesize"] = synthesize
# </solution>

# %% [markdown]
# ## 3. Define the Agent Logic
#
# The agent loop:
# 1. Receive User goal.
# 2. Generate Python code to solve it (using `search` and `synthesize`).
# 3. Execute code.
# 4. Return result.

# %%
SYSTEM_PROMPT = """
You are an expert Python programmer and researcher.
Your goal is to answer the user's question by WRITING A PYTHON SCRIPT.

You have access to the following built-in functions:
- `search(query: str) -> str`: Search the web.
- `synthesize(content: str) -> str`: Summarize information.
- `print(obj)`: Print to stdout (visible to you).

Internal Logic/Plan:
1. Break down the user's request.
2. Search for necessary information (you can call `search` multiple times).
3. Synthesize the findings if needed.
4. Print the final answer clearly.

Output ONLY the Python code. Do not wrap in markdown blocks if possible, or I will strip them.
"""


def run_coding_agent(user_query: str):
    print(f"--- [Agent] Goal: {user_query} ---")

    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_query)]

    # Exercise 7.3: Implement the generation and execution
    # 1. Invoke LLM to get code.
    # 2. Clean code (strip ```python ... ```).
    # 3. Execute using `interpreter`.
    # <solution>
    # 1. Generate Code
    response = llm.invoke(messages)
    code = response.content

    # 2. Clean Code
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    print(f"--- [Agent] Generated Code ---\n{code}\n----------------------------")

    # 3. Execute
    try:
        # LocalPythonExecutor call returns the value of the last expression or print capture
        # smolagents uses `interpreter(...)`
        result = interpreter(code)

        # We also capture stdout usually, but let's see what it returns
        # Combine return value and any captured prints
        captured_stdout = interpreter.state.get("_print_outputs", "")

        final_output = f"Stdout:\n{captured_stdout}\n\nReturn Value:\n{result}"
        return final_output

    except Exception as e:
        return f"Execution Code Error: {e}"
    # </solution>


# %%
# Run the agent
if __name__ == "__main__":
    query = (
        "What is the 10th Fibonacci number (where F1=0, F2=1) multiplied by "
        "the square root of the birth year of the current Microsoft CEO? "
        "Use the 'delegate_code_task' tool to perform the calculation using Python. "
        "Round the final answer to 2 decimal places."
    )
    result = run_coding_agent(query)
    print(f"\n=== FINAL OUTPUT ===\n{result}")
    # should be 2439.55
