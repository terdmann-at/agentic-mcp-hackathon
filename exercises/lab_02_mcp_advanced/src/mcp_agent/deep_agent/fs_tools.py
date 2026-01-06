import os
from pathlib import Path
from langchain_core.tools import tool

# Sandbox configuration
SANDBOX_ROOT = Path("data/deep_agent_sandbox").resolve()


def _get_safe_path(file_path: str) -> Path:
    """Resolve and verify path is within sandbox."""
    # Create sandbox if it doesn't exist
    SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)

    target = (SANDBOX_ROOT / file_path).resolve()
    if not str(target).startswith(str(SANDBOX_ROOT)):
        raise ValueError(f"Access denied: {file_path} is outside the sandbox.")
    return target


@tool
def list_files(directory: str = ".") -> str:
    """List files in the specified directory within the sandbox."""
    try:
        target_dir = _get_safe_path(directory)
        if not target_dir.exists():
            return "Directory does not exist."

        items = os.listdir(target_dir)
        if not items:
            return "Directory is empty."

        return "\n".join(items)
    except Exception as e:
        return f"Error listing files: {str(e)}"


@tool
def read_file(file_path: str) -> str:
    """Read the content of a file."""
    try:
        target_file = _get_safe_path(file_path)
        if not target_file.exists():
            return f"File {file_path} does not exist."

        return target_file.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"


@tool
def write_file(file_path: str, content: str) -> str:
    """Write content to a file. Overwrites if exists."""
    try:
        target_file = _get_safe_path(file_path)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file {file_path}: {str(e)}"


@tool
def edit_file(file_path: str, old_text: str, new_text: str) -> str:
    """Replace occurrences of old_text with new_text in the file."""
    try:
        target_file = _get_safe_path(file_path)
        if not target_file.exists():
            return f"File {file_path} does not exist."

        content = target_file.read_text(encoding="utf-8")
        if old_text not in content:
            return "Error: old_text not found in file."

        new_content = content.replace(old_text, new_text)
        target_file.write_text(new_content, encoding="utf-8")
        return f"Successfully edited {file_path}"
    except Exception as e:
        return f"Error editing file {file_path}: {str(e)}"


fs_tools = [list_files, read_file, write_file, edit_file]
