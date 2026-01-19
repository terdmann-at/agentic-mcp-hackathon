# %% [markdown]
# # Exercise 3: Tool Calling
#
# Goal: Use LangChain to call a custom tool and handle the response.
#

# %%
# %pip install langchain databricks-langchain
# %restart_python

# %%
from databricks_langchain import ChatDatabricks
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import tool

# %%
model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5")


# %% [markdown]
# ## Tools
#
# Tools are simply python functions that are wrapped by the `@tool` decorator.
#
# The decorator takes care of translating the docstring and the types of the inputs into instructions
# for the LLM when given the tool. The LLM does not call the function itself, instead it responds
# with a json structure representing a call to the function, which we will


# %%
# Exercise 3.1: Define a tool using the decorator
# <solution>
@tool
# </solution>
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    if "Berlin" in location:
        return "Cloudy, 15C"
    return "Sunny, 25C"


# %%
def main():
    tools = [get_weather]
    tools_by_name = {t.name: t for t in tools}

    # Exercise 3.2: Bind the tool to the model. Use the .bind_tools method.
    # <solution>
    model_with_tools = model.bind_tools(tools)
    # </solution>

    query = "What is the weather in Berlin?"
    messages = [HumanMessage(content=query)]

    # Exercise 3.3: Invoke the model to get the tool call
    # <solution>
    ai_msg = model_with_tools.invoke(messages)
    # </solution>
    messages.append(ai_msg)
    print(f"AI Call: {ai_msg.tool_calls}")

    # Exercise 3.4: Execute tool calls manually and append results
    for tool_call in ai_msg.tool_calls:
        selected_tool = tools_by_name[tool_call["name"]]

        # Invoke the selected tool
        # <solution>
        tool_output = selected_tool.invoke(tool_call["args"])
        # </solution>
        print(f"Tool Output: {tool_output}")

        messages.append(ToolMessage(content=tool_output, tool_call_id=tool_call["id"]))

    # Exercise 3.5: Get the final response
    # <solution>
    final_response = model_with_tools.invoke(messages)
    # </solution>
    print(f"Final Answer: {final_response.content}")


if __name__ == "__main__":
    main()
