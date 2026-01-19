# %% [markdown]
# # Lab 1: Deep Research Agent with Multi-Agent System
#
# In this lab, we will build a "Deep Research" agent.
# This agent will take a topic, break it down into sub-topics, research them in parallel, and compile a final report.
#
# We will use `LangGraph` for orchestration and `Databricks` Model Serving for the LLM.
#
# ## Structure
# 1. **State Definition**: define the data structure that flows through the graph.
# 2. **Nodes**: define the agents (Chief Editor, Researcher, Writer).
# 3. **Graph**: connect the nodes.
# 4. **Human-in-the-Loop**: add a planning phase with interrupts.
#
# First, let's install the dependencies.

# %%
# %pip install langchain langgraph duckduckgo-search databricks-langchain pydantic typing_extensions
# %restart_python

# %% [markdown]
# ## Setup
# Import necessary libraries and initialize the LLM and Tools.

# %%
import operator
from typing import Annotated, List, TypedDict

try:
    from typing import NotRequired
except ImportError:
    from typing_extensions import NotRequired

from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, Send, interrupt

# Initialize Model
from llm import model as llm
from pydantic import BaseModel, Field

# Initialize Search Tool
search_tool = DuckDuckGoSearchRun()

# %% [markdown]
# ## Exercise 1: State Definition
#
# We need to define the state that holds our research data.
#
# The `ResearchState` should track:
# - `topic`: The user's original query.
# - `sub_topics`: A list of strings for parallel research.
# - `research_outputs`: A list of results from workers (this needs to be cumulative!).
# - `final_report`: The generated output.
#
# The `SubTaskState` is for individual workers and needs:
# - `topic`: The specific sub-topic to research.


# %%
# Exercise 1: Define the State classes
# <solution>
class SubTaskState(TypedDict):
    """State for a single research worker agent."""

    topic: str
    result: str


class ResearchState(TypedDict):
    """Global state for the entire graph."""

    topic: str
    sub_topics: List[str]
    # Use operator.add to append new outputs to the list instead of overwriting
    research_outputs: Annotated[List[str], operator.add]
    final_report: str


# </solution>


class ResearchPlan(BaseModel):
    """Structured output for the Chief Editor."""

    sub_topics: List[str] = Field(
        description="List of 3 distinct sub-topics to research in parallel"
    )


# %% [markdown]
# ## Exercise 2: Define Nodes
#
# We need three nodes:
#
# 1. **Chief Editor**: breaks the topic into sub-topics.
# 2. **Research Worker**: searches for information on a sub-topic.
# 3. **Writer**: compiles the report.


# %%
def chief_editor_node(state: ResearchState):
    print(f"--- [Chief Editor] Planning: {state['topic']} ---")

    # Exercise 2.1: Implement the Chief Editor
    # Use the LLM to generate a 'ResearchPlan' from the topic.
    # <solution>
    planner = llm.with_structured_output(ResearchPlan)
    prompt = (
        f"You are a Research Manager. Your goal is to break down the following research topic into 3 distinct, "
        f"targeted sub-topics that will convince a search engine to reveal specific facts, numbers, or data points.\n\n"
        f"Topic: {state['topic']}\n\n"
        f"Return 3 distinct sub-topics."
    )
    plan = planner.invoke(prompt)

    return {"sub_topics": plan.sub_topics}
    # </solution>


def research_worker_node(state: SubTaskState):
    topic = state["topic"]
    print(f"--- [Worker] Searching for: {topic} ---")

    # Exercise 2.2: Implement the Research Worker
    # Use 'search_tool' to find info and return it in 'research_outputs'.
    # <solution>
    try:
        res = search_tool.invoke(topic)
    except Exception as e:
        res = f"Search failed: {e}"

    return {"research_outputs": [f"## Subtopic: {topic}\n{res}\n"]}
    # </solution>


def writer_node(state: ResearchState):
    print("--- [Writer] Compiling Report ---")

    # Exercise 2.3: Implement the Writer
    # Combine 'research_outputs' and ask the LLM to write a report.
    # <solution>
    combined_content = "\n\n".join(state["research_outputs"])

    prompt = f"""
    You are a technical writer. Compile the following research notes into a comprehensive final report.

    Topic: {state["topic"]}

    Research Notes:
    {combined_content}

    Instructions:
    1. Synthesize the information into a clear, well-structured report.
    2. End with a "Final Answer:" section.
    """

    response = llm.invoke(prompt)
    return {"final_report": response.content}
    # </solution>


# %% [markdown]
# ## Exercise 3: Graph Construction
#
# Now we wire them together.
#
# - **Start** -> **Chief Editor**
# - **Chief Editor** -> **Workers** (Conditional Edge using `Send`)
# - **Workers** -> **Writer**
# - **Writer** -> **End**


# %%
def map_subtopics(state: ResearchState):
    # Exercise 3.1: Define the mapping logic
    # Return a list of `Send` objects, one for each sub-topic.
    # <solution>
    return [
        Send("research_worker", {"topic": sub_topic})
        for sub_topic in state["sub_topics"]
    ]
    # </solution>


# Exercise 3.2: Build the Graph
# <solution>
workflow = StateGraph(ResearchState)

workflow.add_node("chief_editor", chief_editor_node)
workflow.add_node("research_worker", research_worker_node)
workflow.add_node("writer", writer_node)

workflow.add_edge(START, "chief_editor")
workflow.add_conditional_edges("chief_editor", map_subtopics, ["research_worker"])
workflow.add_edge("research_worker", "writer")
workflow.add_edge("writer", END)

# Compile the graph
app = workflow.compile()
# </solution>

# %% [markdown]
# ### Run the Graph (Basic)

# %%
res = app.invoke({"topic": "The future of Agentic AI"})
print(res["final_report"])

# %% [markdown]
# ## Exercise 4: Human-in-the-Loop (Planning Phase)
#
# Real-world agents need supervision. Let's add a "Planning Phase" where the user can review and edit the sub-topics before research begins.
#
# We will implement a cycle in the graph:
# 1. **Planner**: generates an initial plan (or regenerates based on feedback).
# 2. **Reviewer**: interrupts execution to request user approval.
# 3. **Conditional Edge**:
#    - If approved -> proceed to **Research Workers**.
#    - If rejected (with critique) -> loop back to **Planner**.


# %%
# Define new state for HITL
class ResearchStateHITL(ResearchState):
    critique: NotRequired[str]
    approved: NotRequired[bool]


def planner_node(state: ResearchStateHITL):
    print(f"--- [Planner] Planning: {state['topic']} ---")

    planner = llm.with_structured_output(ResearchPlan)

    # If there is a critique, we are regenerating
    if state.get("critique"):
        print(f"--- [Planner] Regenerating with critique: {state.get('critique')} ---")
        prompt = f"""
        Original Topic: {state["topic"]}
        Previous Plan: {state.get("sub_topics")}
        User Critique: {state.get("critique")}

        Generate a new plan with 3 distinct sub-topics that addresses the critique.
        """
    else:
        # Initial plan
        prompt = f"Topic: {state['topic']}\nReturn 3 distinct sub-topics."

    plan = planner.invoke(prompt)
    return {"sub_topics": plan.sub_topics, "approved": False}


def reviewer_node(state: ResearchStateHITL):
    # Exercise 4: Add the interrupt
    # <solution>
    # Interrupt and wait for feedback
    # We allow the user to provide {"approved": True} or {"critique": "..."}
    feedback = interrupt(
        {
            "sub_topics": state["sub_topics"],
            "message": "Please review the research plan. Provide 'approved': True or 'critique': str.",
        }
    )
    # The feedback from resume is expected to update the state
    return feedback
    # </solution>


def should_continue(state: ResearchStateHITL):
    """
    Conditional edge logic:
    - If approved -> Map to research workers
    - If not approved -> Loop back to planner
    """
    if state.get("approved"):
        # Map to workers
        return [
            Send("research_worker", {"topic": sub_topic})
            for sub_topic in state["sub_topics"]
        ]

    # Loop back
    return "planner"


# %% [markdown]
# ### Re-build the Graph with HITL
# The logic is now explicit in the graph structure:
# `Planner` -> `Reviewer` -> (conditional) -> `Planner` or `Workers`.

# %%
from langgraph.checkpoint.memory import InMemorySaver

# Re-define graph
workflow_hitl = StateGraph(ResearchStateHITL)

workflow_hitl.add_node("planner", planner_node)
workflow_hitl.add_node("reviewer", reviewer_node)
workflow_hitl.add_node("research_worker", research_worker_node)
workflow_hitl.add_node("writer", writer_node)

# Start -> Planner
workflow_hitl.add_edge(START, "planner")

# Planner -> Reviewer
workflow_hitl.add_edge("planner", "reviewer")

# Reviewer -> Conditional (Planner or Workers)
workflow_hitl.add_conditional_edges(
    "reviewer", should_continue, ["planner", "research_worker"]
)

workflow_hitl.add_edge("research_worker", "writer")
workflow_hitl.add_edge("writer", END)

# Compile with checkpointer
checkpointer = InMemorySaver()
app_hitl = workflow_hitl.compile(checkpointer=checkpointer)

# %% [markdown]
# ### Run Interactive Session
#
# We need to handle the execution flow:
# 1. Run until interrupt.
# 2. Inspect payload.
# 3. Resume with feedback.


# %%
def run_research_interactive():
    """
    Runs the research agent in an interactive loop.
    Allows the user to review the plan and provide feedback.
    """
    # 1. Setup
    thread_id = "research-thread-interact"
    config = {"configurable": {"thread_id": thread_id}}

    print("Welcome to the Deep Research Agent!")
    topic = input("Enter a research topic: ")

    # We use a loop to handle the stream and inputs
    # Initial input is the topic
    current_input = {"topic": topic}
    resume_command = None

    while True:
        # If we have a resume command (from the 2nd loop onwards), use it
        if resume_command:
            stream_input = resume_command
        else:
            stream_input = current_input

        # Run the graph until it interrupts or finishes
        # We need to stream to capture interrupts
        events = app_hitl.stream(stream_input, config=config)

        current_interrupt_value = None
        final_report = None

        print("\n--- Agent Working ---")
        for event in events:
            # Check for interrupt
            if "__interrupt__" in event:
                current_interrupt_value = event["__interrupt__"][0].value

            # Check for writer output (final step)
            if "writer" in event:
                final_report = event["writer"].get("final_report")

        # A. If we got a final report, we are done
        if final_report:
            print("\n" + "=" * 40)
            print("FINAL REPORT")
            print("=" * 40)
            print(final_report)
            break

        # B. If we hit an interrupt, ask for user feedback
        if current_interrupt_value:
            print("\n" + "-" * 40)
            print("REVIEW PLAN")
            print("-" * 40)
            print(f"Proposed Sub-topics: {current_interrupt_value['sub_topics']}")

            user_response = input(
                "\nType 'ok' to approve, or enter your critique/changes: "
            ).strip()

            if user_response.lower() in ["ok", "yes", "approve"]:
                print("\n> Approved. Proceeding to research...")
                resume_command = Command(resume={"approved": True})
            else:
                print("\n> Critique received. Regenerating plan...")
                resume_command = Command(
                    resume={"approved": False, "critique": user_response}
                )


# %%
# Run the interactive session
run_research_interactive()


# %% [markdown]
# ## Exercise 5 (Bonus): Benchmark Evaluation (GAIA)
#
# We will now evaluate our agent against some questions from the GAIA benchmark.
# We compare the Deep Research Agent against a standard ReAct baseline.
#
# Your task is to play with the prompt, or the structure of the system to improve the score.

# %%
import re

import pandas as pd
from ddgs import DDGS
from langchain import tool
from langchain.agents import create_agent


@tool
def web_search(query: str, max_results: int = 5):
    """Run a web search"""
    return str(DDGS().text(query, max_results=max_results))


# 1. Setup ReAct Baseline
agent_react = create_agent(llm, [web_search])

# 2. Load Dataset
# Ensure create_gaia_dataset() has been run or the file exists.
csv_path = "gaia_validation_level1.csv"
try:
    filtered_df = pd.read_csv(csv_path)[:2]
    print(f"Loaded {len(filtered_df)} tasks for evaluation.")
except FileNotFoundError:
    print(
        f"Dataset not found at {csv_path}. Please run 'python src/create_gaia.py' inside labs/ directory."
    )
    filtered_df = pd.DataFrame()


# 3. Define Judge
def query_judge_model(question, predicted, truth, metadata):
    prompt = f"""
    You are an impartial judge.

    [CONTEXT/METADATA]: {metadata}
    [QUESTION]: {question}
    [GROUND TRUTH]: {truth}
    [PREDICTED]: {predicted}

    Compare Predicted to Ground Truth. Assign a score 1-10.
    1 = Wrong, 10 = Perfect.
    Also provide a short explanation.

    Output format:
    SCORE: [Score]
    REASON: [Short explanation]
    """
    try:
        return llm.invoke(prompt).content
    except Exception as e:
        return f"SCORE: 0 REASON: Error calling judge: {e}"


def extract_score(judge_response):
    match = re.search(r"SCORE:\s*(\d+)", judge_response)
    return int(match.group(1)) if match else 0


# 4. Evaluation Loop
results = []
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        task_id = row["task_id"]
        question = row["Question"]
        truth = row["Final answer"]
        metadata = str(row["Annotator Metadata"])

        print(f"\nProcessing Task: {task_id}")

        # --- Agent 1: Deep Research (Our App) ---
        try:
            # We use the autonomous 'app' from Exercise 3
            result_dr = app.invoke({"topic": question})
            predicted_dr = result_dr.get("final_report", "No report generated.")
        except Exception as e:
            predicted_dr = f"Error during research: {str(e)}"
        print(f"[Deep Research Output]: {predicted_dr[:100]}...")

        judge_resp_dr = query_judge_model(question, predicted_dr, truth, metadata)
        score_dr = extract_score(judge_resp_dr)
        print(f"Deep Research Score: {score_dr}")

        # --- Agent 2: ReAct Baseline ---
        print("[ReAct] Researching...")
        try:
            result_react = react_executor.invoke({"input": question})
            predicted_react = result_react.get("output", "No output")
        except Exception as e:
            predicted_react = f"Error during ReAct: {str(e)}"
        print(f"[ReAct Output]: {predicted_react[:100]}...")

        judge_resp_react = query_judge_model(question, predicted_react, truth, metadata)
        score_react = extract_score(judge_resp_react)
        print(f"ReAct Score: {score_react}")

        results.append(
            {
                "task_id": task_id,
                "question": question,
                "ground_truth": truth,
                "deep_research_pred": predicted_dr,
                "deep_research_score": score_dr,
                "react_pred": predicted_react,
                "react_score": score_react,
            }
        )

    # 5. Results
    results_df = pd.DataFrame(results)
    print("\n=== Evaluation Results ===")
    print(results_df)
