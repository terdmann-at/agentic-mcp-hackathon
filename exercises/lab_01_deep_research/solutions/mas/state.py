import operator
from typing import Annotated, List, TypedDict, Union
from pydantic import BaseModel, Field

# --- MAS State Definitions ---

class SubTaskState(TypedDict):
    """State for a single research worker agent."""
    topic: str
    result: str

class ResearchState(TypedDict):
    """Global state for the entire graph."""
    topic: str
    # The breakdown of the topic into sub-topics
    sub_topics: List[str]
    # The collected results from parallel workers
    # We use a reducer (operator.add) to merge lists returned by parallel nodes
    research_outputs: Annotated[List[str], operator.add]
    final_report: str

class ResearchPlan(BaseModel):
    """Structured output for the Chief Editor."""
    sub_topics: List[str] = Field(description="List of 3 distinct sub-topics to research in parallel")
