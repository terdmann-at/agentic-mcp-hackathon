# %% [markdown]
# # Exercise 3: Tool Calling
# 
# Goal: Use LangChain and OpenAI to call a custom tool.


# %%
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)


# %%
# <solution>
@tool
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    # Mock response
    if "Berlin" in location:
        return "Cloudy, 15C"
    return "Sunny, 25C"

tools = [get_weather]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)
# </solution>


# %%
query = "What is the weather in Berlin?"
messages = [HumanMessage(content=query)]

# 1. Model decides to call a tool
ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)
print(f"AI Call: {ai_msg.tool_calls}")


# %% [markdown]
# ### Solution
# Executing the tool and passing back the result.


# %%
# <solution>
# 2. Execute tool calls
for tool_call in ai_msg.tool_calls:
    selected_tool = tools_by_name[tool_call["name"]]
    tool_output = selected_tool.invoke(tool_call["args"])
    print(f"Tool Output: {tool_output}")

    # Append tool output to history
    messages.append(ToolMessage(content=tool_output, tool_call_id=tool_call["id"]))
# </solution>

# 3. Get final response
final_response = model_with_tools.invoke(messages)
print(f"Final Answer: {final_response.content}")

