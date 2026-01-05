from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    The state of our ReAct agent.
    It simply holds a list of messages.
    """
    messages: Annotated[list[BaseMessage], add_messages]
