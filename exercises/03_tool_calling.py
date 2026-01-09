# %% [markdown]
# # Exercise 3: Tool Calling
#
# Goal: Use LangChain and OpenAI to call a custom tool.
#
# To test your solution, run:
#
#       uv run 03_tool_calling.py
#

# %%
from dotenv.main import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI

load_dotenv()

model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)


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


def main():
    tools = [get_weather]
    tools_by_name = {t.name: t for t in tools}

    # Exercise 3.2: Bind the tool to the model
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

    # 2. Execute tool calls manually
    for tool_call in ai_msg.tool_calls:
        selected_tool = tools_by_name[tool_call["name"]]
        
        # Exercise 3.4: Invoke the selected tool
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
