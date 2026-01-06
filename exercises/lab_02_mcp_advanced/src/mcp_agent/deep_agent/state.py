from typing import List, TypedDict, Annotated, Optional
from langchain_core.messages import BaseMessage
import operator


class ToDo(TypedDict):
    task: str
    status: str  # "pending", "in_progress", "completed"
    subtasks: List[str]


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    todos: List[ToDo]
    sandbox_dir: str
    # Track the current active task from the todo list
    current_todo_index: Optional[int]
