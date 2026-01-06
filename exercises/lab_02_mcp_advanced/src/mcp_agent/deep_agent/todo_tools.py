from typing import List
from langchain_core.tools import tool


@tool
def write_todos(todos: List[str]) -> str:
    """Create or overwrite the todo list.
    Args:
        todos: A list of task descriptions.
    """
    # The actual state update happens in the graph node when this tool is detected
    # This tool function mainly serves as a schema definition for the LLM
    return f"Plan updated with {len(todos)} tasks."


@tool
def mark_todo_completed(index: int) -> str:
    """Mark a todo item as completed by its index (0-based)."""
    # Similarly, state update happens in the graph
    return f"Task {index} marked as completed."


todo_tools = [write_todos, mark_todo_completed]
