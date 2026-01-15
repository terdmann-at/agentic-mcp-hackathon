import operator
from typing import Annotated, List, TypedDict

import streamlit as st
from databricks_langchain import ChatDatabricks
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from pydantic import BaseModel, Field

# --- Initial Setup ---
st.set_page_config(layout="wide")

# Setup LLM and Tools
try:
    # Use the model from the initial setup
    llm = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5")
except Exception as e:
    st.error(f"Failed to initialize ChatDatabricks: {e}")
    st.stop()

# Initialize Search Tool
try:
    search_tool = DuckDuckGoSearchRun()
except Exception as e:
    st.warning(
        f"Failed to initialize search tool: {e}. Search functionality may not work."
    )
    search_tool = None  # Handle gracefully or let it fail later

# --- State Definitions ---


class SubTaskState(TypedDict):
    """State for a single research worker agent."""

    topic: str
    result: str


class ResearchState(TypedDict):
    """Global state for the entire graph."""

    topic: str
    sub_topics: List[str]
    research_outputs: Annotated[List[str], operator.add]
    final_report: str


class ResearchPlan(BaseModel):
    """Structured output for the Chief Editor."""

    sub_topics: List[str] = Field(
        description="List of 3 distinct sub-topics to research in parallel"
    )


# --- Nodes ---


def chief_editor_node(state: ResearchState):
    """
    The 'Manager': Breaks the user's topic into sub-topics for parallel research.
    """
    topic = state.get("topic", "")

    # Use structured output for planning
    planner = llm.with_structured_output(ResearchPlan)
    prompt = (
        f"You are a Research Manager. Your goal is to break down the following research topic into 3 distinct, "
        f"targeted sub-topics that will convince a search engine to reveal specific facts, numbers, or data points.\n\n"
        f"Topic: {topic}\n\n"
        f"Return 3 to 5 distinct sub-topics."
    )
    plan = planner.invoke(prompt)

    return {"sub_topics": plan.sub_topics}


def research_worker_node(state: SubTaskState):
    """
    The 'Worker': Takes a single sub-topic, searches, and returns the result.
    """
    topic = state["topic"]

    if not search_tool:
        return {
            "research_outputs": [f"## Subtopic: {topic}\nSearch tool not available.\n"]
        }

    try:
        res = search_tool.invoke(topic)
    except Exception as e:
        res = f"Search failed: {e}"

    return {"research_outputs": [f"## Subtopic: {topic}\n{res}\n"]}


def writer_node(state: ResearchState):
    """
    The 'Writer': Compiles all research outputs into a final report.
    """
    combined_content = "\n\n".join(state["research_outputs"])

    prompt = f"""
    You are a technical writer. Compile the following research notes into a comprehensive final report.
    
    Topic: {state["topic"]}
    
    Research Notes:
    {combined_content}
    
    Instructions:
    1. Synthesize the information into a clear, well-structured report.
    2. If the original topic asked for a specific format (e.g. list, number, zip code), ensure you explicitly provide it.
    3. MANDATORY: You MUST end the report with a section labeled exactly "Final Answer:" containing the specific answer to the user's question, without extra commentary.
    
    Report:
    """

    response = llm.invoke(prompt)
    return {"final_report": response.content}


# --- Graph Definition ---


def map_subtopics(state: ResearchState):
    """
    Conditional edge function that maps sub-topics to parallel worker calls.
    Returns a list of Send objects.
    """
    return [
        Send("research_worker", {"topic": sub_topic})
        for sub_topic in state["sub_topics"]
    ]


# Initialize Graph
workflow = StateGraph(ResearchState)

# Add Nodes
workflow.add_node("chief_editor", chief_editor_node)
workflow.add_node("research_worker", research_worker_node)
workflow.add_node("writer", writer_node)

# Add Edges
workflow.add_edge(START, "chief_editor")
workflow.add_conditional_edges("chief_editor", map_subtopics, ["research_worker"])
workflow.add_edge("research_worker", "writer")
workflow.add_edge("writer", END)

# Compile
mas_app = workflow.compile()

# --- Application UI ---

st.title("🔍 Deep Research AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to research?"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Researching... (This may take a moment)"):
            try:
                initial_state = {
                    "topic": prompt,
                    "sub_topics": [],
                    "research_outputs": [],
                    "final_report": "",
                }

                result = mas_app.invoke(initial_state)
                response_content = result.get("final_report", "No report generated.")

                st.markdown(response_content)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_content}
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
