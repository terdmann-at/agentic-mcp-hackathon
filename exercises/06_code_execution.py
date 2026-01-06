# %% [markdown]
# # Exercise 6: Code Execution vs Tool Calling
#
# Goal: Use `smolagents` to implement an agent that writes code to solve problems.
# Compare this approach to the standard ReAct tool-calling loop (Exercise 4).
#
# Prerequisites: `uv add smolagents`

# %%
from smolagents import AzureOpenAIModel, CodeAgent

# 1. Setup the Model
# We use the native AzureOpenAIModel from smolagents.
# This expects the following environment variables to be set:
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_ENDPOINT
# - OPENAI_API_VERSION
#
model = AzureOpenAIModel(
    model_id="gpt-4.1",  # Your deployment name
    temperature=0.7,  # Optional parameters
)

# %% [markdown]
# ### Part 1: Basic Code Execution
# `smolagents` allows the LLM to write Python code which is then executed in a local sandbox.

# %%

# Create an agent that uses code execution
# We grant it access to additional base tools if needed, but the core power is the Python executor.
agent = CodeAgent(tools=[], model=model, add_base_tools=True)

print("Solving simple math...")
agent.run("What is the 10th fibonacci number?")

# %% [markdown]
# ### Part 2: Efficiency Comparison
# In Exercise 4, we calculated:
# `((144 / 12) * (25 + 75)) / ((10 * 10) / (500 / 5)) + ((81 / 9) * (121 / 11))`
#
# Using a ReAct agent with basic `add`, `multiply`, `divide` tools, this required **many** round-trips (LLM call -> Tool call -> LLM call -> ...).
#
# Let's see how a Code Agent handles it.

# %%
complex_math_query = "Calculate ((144 / 12) * (25 + 75)) / ((10 * 10) / (500 / 5)) + ((81 / 9) * (121 / 11))"

print(f"\nSolving complex math: {complex_math_query}")
result = agent.run(complex_math_query)

print(f"\nResult: {result}")

# %% [markdown]
# ### Analysis
#
# **Tool Calling / ReAct (Exercise 4):**
# *   Step 1: Divide 144 / 12 -> 12
# *   Step 2: Add 25 + 75 -> 100
# *   Step 3: Multiply 12 * 100 -> 1200
# *   ... and so on.
# *   **Total steps:** ~10+ API calls. Slow, expensive, prone to losing context.
#
# **Code Execution (Exercise 6):**
# *   Step 1: Write a Python script: `print(((144 / 12) * (25 + 75)) / ...)`
# *   Step 2: Execute.
# *   **Total steps:** 1 API call. Fast, cheap, exact.
#
# **Takeaway:** For logic, math, and data tasks, allowing the agent to *write code* is often vastly superior to giving it granular tools.
