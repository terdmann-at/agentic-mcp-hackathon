# %% [markdown]
# # Exercise 5: Web Automation & Vision Agent
#
# Goal: Build a visual web browsing agent using Helium and LangGraph.
#
# This agent will be able to navigate the web, see screenshots, and interact with elements.
#
# To test your solution, run:
#
#       uv run 05_web_automation.py
#

# %%
import base64
import operator
import time
from typing import Annotated, TypedDict, Optional

from dotenv.main import load_dotenv
from helium import start_chrome, go_to, click, write, get_driver
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


load_dotenv()

# Setup simplified Helium Navigator
class HeliumNavigator:
    _instance = None
    def __init__(self):
        self._is_initialized = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = HeliumNavigator()
        return cls._instance

    def initialize(self):
        if not self._is_initialized:
            # We use headless=False so you can see what's happening!
            start_chrome(headless=False)
            self._is_initialized = True

    def get_screenshot_b64(self) -> str:
        self.initialize()
        driver = get_driver()
        return driver.get_screenshot_as_base64()

    def navigate(self, url: str) -> str:
        self.initialize()
        go_to(url)
        time.sleep(2)
        return f"Navigated to {url}."

    def click_element(self, target: str) -> str:
        self.initialize()
        click(target)
        time.sleep(1)
        return f"Clicked '{target}'."

    def type_text(self, text: str) -> str:
        self.initialize()
        write(text)
        time.sleep(1)
        return f"Typed '{text}'."

navigator = HeliumNavigator.get_instance()

# %%
# Exercise 5.1: Define Tools
# We will wrap the navigator methods into tools.
# Note: get_screenshot returns the base64 string directly for the agent to "see".

@tool
def navigate(url: str) -> str:
    """Navigate the browser to a specific URL."""
    return navigator.navigate(url)

@tool
def click_element(target: str) -> str:
    """Click an element. 'target' can be the visible text on the button/link."""
    return navigator.click_element(target)

@tool
def type_text(text: str) -> str:
    """Type text into the focused element."""
    return navigator.type_text(text)

# <solution>
@tool
def get_screenshot() -> str:
    """Get the current page screenshot as a base64 string."""
    return navigator.get_screenshot_b64()
# </solution>

tools = [navigate, click_element, type_text, get_screenshot]
tools_by_name = {tool.name: tool for tool in tools}

model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
model_with_tools = model.bind_tools(tools)


# %%
# State Definition
class VisualState(TypedDict):
    # We store the conversation history
    messages: Annotated[list[BaseMessage], add_messages]
    # We also store the latest screenshot to present it to the model
    # simplified: we will inject it into the message history manually
    screenshot: str 


# Exercise 5.2: Define Custom Tool Node
# This node executes tools. If the tool is `get_screenshot`, it handles the base64 output
# by creating a multimodal ToolMessage.

def tool_node(state: VisualState):
    messages = state["messages"]
    last_message = messages[-1]
    results = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        call_id = tool_call["id"]
        
        selected_tool = tools_by_name[tool_name]
        
        # Invoke the tool
        output = selected_tool.invoke(tool_args)
        
        # <solution>
        # Special handling for screenshot to make it visible to the model
        if tool_name == "get_screenshot":
            # output is the base64 string
            content = [
                {"type": "text", "text": "Here is the screenshot of the current page."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{output}"}}
            ]
            results.append(ToolMessage(content=content, tool_call_id=call_id))
        else:
            # Standard text output
            results.append(ToolMessage(content=str(output), tool_call_id=call_id))
        # </solution>
    
    return {"messages": results}


# %%
# Agent Node
def agent_node(state: VisualState):
    # The model deals with the history of messages which now includes images
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state: VisualState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# %%
def main():
    # Exercise 5.3: Build the Graph
    # Define the nodes and edges for the ReAct architecture.
    
    # <solution>
    workflow = StateGraph(VisualState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    
    app = workflow.compile()
    # </solution>

    # Exercise 5.4: Run the Agent
    # Instruct the agent to perform a visual task.
    
    query = "Go to wikipedia.org. Type 'Agentic AI' into the search bar. Then take a screenshot to verify properly."
    print(f"User: {query}")
    
    # <solution>
    # Note: We stream to see the steps
    inputs = {"messages": [HumanMessage(content=query)]}
    for event in app.stream(inputs, stream_mode="values"):
        message = event["messages"][-1]
        if isinstance(message, AIMessage):
            print(f"AI: {message.content}")
            if message.tool_calls:
                print(f"   Tools: {message.tool_calls}")
        elif isinstance(message, ToolMessage):
            print(f"Tool ({message.name}): [Output received]")
    # </solution>

if __name__ == "__main__":
    main()
