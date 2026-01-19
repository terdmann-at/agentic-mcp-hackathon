# %% [markdown]
# # GAIA Evaluation
#
# This notebook evaluates the Deep Research Agent against the GAIA benchmark.
#

# %%
# %pip install langchain langgraph ddgs databricks-langchain pydantic pandas typing_extensions
# %restart_python

# %%
import re

import pandas as pd
from deep_research_app import app as research_agent
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun

from llm import model as judge_llm
from llm import model as llm

react_agent = create_agent(llm, [DuckDuckGoSearchRun()])
filtered_df = pd.read_csv("gaia_validation_level1.csv")[:5]

print(f"Loaded {len(filtered_df)} tasks for evaluation.")


# 3. Define Judge Wrapper
def query_judge_model(question, predicted, truth, metadata):
    """
    Evaluates the answer using the Judge LLM.
    """
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
    return judge_llm.invoke(prompt).content


def extract_score(judge_response):
    match = re.search(r"SCORE:\s*(\d+)", judge_response)
    return int(match.group(1)) if match else None


# 4. Run Evaluation Loop
results = []
for index, row in filtered_df.iterrows():
    task_id = row["task_id"]
    question = row["Question"]
    truth = row["Final answer"]
    metadata = str(row["Annotator Metadata"])

    print(f"\nProcessing Task: {task_id}")

    # --- Agent 1: Deep Research ---
    result = research_agent.invoke({"topic": question})
    predicted_dr = result.get("final_report")
    print(f"[Deep Research Output]: {predicted_dr[:100]}...")

    judge_resp_dr = query_judge_model(question, predicted_dr, truth, metadata)
    score_dr = extract_score(judge_resp_dr)
    print(f"Deep Research Score: {score_dr}")

    # --- Agent 2: ReAct Baseline ---
    print("[ReAct] Researching...")
    result = react_agent.invoke({"messages": [question]})
    predicted_react = result["messages"][-1].content
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


# 5. Summary
results_df = pd.DataFrame(results)
print("\n=== Evaluation Results ===")
print(results_df)

# Optional: Save to CSV
# results_df.to_csv("gaia_eval_results_pandas.csv", index=False)
