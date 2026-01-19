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
from smolagents import LocalPythonExecutor
from smolagents.local_python_executor import InterpreterError

from llm import llm

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


tools = [exec_python]
agent = create_agent(model=llm, tools=tools)


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
