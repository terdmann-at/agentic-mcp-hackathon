import operator
from typing import Annotated, List, TypedDict

from pydantic import BaseModel, Field

# --- MAS State Definitions ---


class SubTaskState(TypedDict):
    """State for a single research worker agent."""

    topic: str
    result: str


class ResearchState(TypedDict):
    """Global state for the entire graph."""

    topic: str
    # TODO: Add 'sub_topics' list
    # TODO: Add 'research_outputs' with a reducer (operator.add)
    # TODO: Add 'final_report'
    sub_topics: List[str]
    research_outputs: Annotated[List[str], operator.add]
    final_report: str


class ResearchPlan(BaseModel):
    """Structured output for the Chief Editor."""

    sub_topics: List[str] = Field(
        description="List of 3 distinct sub-topics to research in parallel"
    )
