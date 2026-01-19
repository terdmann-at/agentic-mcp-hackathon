# %% [markdown]
# # Exercise 6: Code Execution vs Tool Calling
#
# Here, we will use the `LocalPythonExecutor` class from `smolagents` to implement an agent that writes code to solve problems.
#

# %%
# %pip install smolagents
# %restart_python

# %%
import pandas as pd
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import tool
from llm import model as llm
from smolagents import LocalPythonExecutor
from smolagents.local_python_executor import InterpreterError

df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/refs/heads/master/titanic.csv"
)


interpreter = LocalPythonExecutor(
    additional_authorized_imports=[
        "pandas",
        "matplotlib",
        "sklearn",
        "sklearn.linear_model",
        "matplotlib.pyplot",
        "datetime",
    ],
)
interpreter.send_tools({})
interpreter.state["df"] = df
interpreter("import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt")


# Exercise 6.1: Define the `exec_python` tool
# This tool should take a code string, execute it using the `interpreter`, and return the output.
# <solution>
@tool
def exec_python(code: str):
    """
    Evaluate python code. Can be used to perform calculations.
    The data to analyze is already defined as the variable 'df'.
    """
    try:
        output = interpreter(
            code,
        )
        return f"Stdout:\n{str(interpreter.state['_print_outputs'])}\nOutput: {output}"
    except InterpreterError as e:
        return f"There was an error: {e}"


# </solution>


# Exercise 6.2: Create the agent
# Use `create_agent` with the model and tools.
# <solution>
tools = [exec_python]
agent = create_agent(model=llm, tools=tools)
# </solution>


# %%
# Let's test the agent
response = agent.invoke(
    {
        "messages": [
            HumanMessage(
                # "can you make some descriptive plots of the data and summarize it? avoid seaborn. save the plot"
                "can you make fit a logistc reg for who survived? the data is in df. do not stop until done."
            )
        ]
    }
)

# Print the message history
for msg in response["messages"]:
    if type(msg) is AIMessage and msg.tool_calls:
        print("=" * 20 + " Code " + "=" * 20)
        print(msg.tool_calls[0]["args"]["code"])
        print("=" * 50)
    print(msg.content)
    print("\n")


# %%
# Exercise 6.3: Implement Memory Tools
# We want to give the agent a "long-term memory" to store results and errors.
# We will use LangGraph's InMemoryStore with semantic search capabilities.
#
# 1. Initialize `memory_store` with the embeddings.
# 2. Implement `create_memory(key: str, value: str, category: str)` to add to the store.
# 3. Implement `recall_memory(query: str)` to search the store using semantic search.

import uuid

from langgraph.store.memory import InMemoryStore
from llm import embedding_dimensions, embeddings

# <solution>
# Initialize the store with the embedding model and dimensions
memory_store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": embedding_dimensions,
    }
)


@tool
def create_memory(key: str, value: str, category: str = "result"):
    """
    Stores a piece of information in long-term memory.
    Useful for saving results to avoid re-calculation, or errors to avoid repeating them.

    Args:
        key: A short descriptive key or title for the memory.
        value: The content/details to remember.
        category: The category of memory. Must be either 'result' (for analysis findings) or 'error' (for bugs/issues).
    """
    if category not in ["result", "error"]:
        return "Error: Category must be either 'result' or 'error'."

    # Namespace based on category
    namespace = ("global", category)
    memory_id = str(uuid.uuid4())

    memory_store.put(
        namespace, memory_id, {"key": key, "value": value, "category": category}
    )
    return f"Stored memory {memory_id} in category '{category}'"


@tool
def recall_memory(query: str, category: str = "result"):
    """
    Retrieves information from long-term memory based on a query.

    Args:
        query: Search term to find relevant memories using semantic search.
        category: The category to search in. use 'result' for past analysis, 'error' for coding patterns/restrictions.
    """
    namespace = ("global", category)
    # Search for top 3 most relevant memories
    results = memory_store.search(namespace, query=query, limit=3)

    if not results:
        return f"No relevant memories found in category '{category}'."

    formatted_results = []
    for item in results:
        content = item.value
        formatted_results.append(
            f"[{content['category']}] {content['key']}: {content['value']}"
        )

    return "Found memories:\n" + "\n".join(formatted_results)


# </solution>


# %%
# Exercise 6.4: Create an Agent with Memory
# Create a new agent that has access to `exec_python`, `create_memory`, and `recall_memory`.
# Ask it to perform a calculation, store the result, and then in a follow-up ("later"), ask it to recall it.

# <solution>
memory_tools = [exec_python, create_memory, recall_memory]
memory_agent = create_agent(model=llm, tools=memory_tools)
# </solution>

# %%
# Test the memory agent
print("--- Testing Memory Agent ---")

# Step 1: Perform a task and remember the result
response1 = memory_agent.invoke(
    {
        "messages": [
            HumanMessage(
                "Calculate the mean age of passengers in the Titanic dataset (variable 'df'). "
                "Store the result in your memory so you don't have to calculate it again."
            )
        ]
    }
)
print(response1["messages"][-1].content)

# Step 2: Ask a question that requires recalling the memory
print("\n--- Testing Recall ---")
response2 = memory_agent.invoke(
    {
        "messages": [
            HumanMessage(
                "Do you remember the mean age of the passengers? "
                "Try recalling past analyses."
            )
        ]
    }
)
print(response2["messages"][-1].content)

# %%
# Print the message history
for msg in response2["messages"]:
    if type(msg) is AIMessage and msg.tool_calls:
        print("=" * 20 + " Code " + "=" * 20)
        if "code" in msg.tool_calls[0]["args"]:
            print(msg.tool_calls[0]["args"]["code"])
        print("=" * 50)
    print(msg.content)
    print("\n")
