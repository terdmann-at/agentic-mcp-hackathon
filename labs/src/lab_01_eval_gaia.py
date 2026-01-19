import re
import pandas as pd
from datasets import load_dataset
from huggingface_hub import snapshot_download

# Import the configured model (Judge) and the Agent Application (Solver)
from llm import model as judge_llm
from lab_01_deep_research import app

# 1. Load GAIA Validation Set
print("Loading GAIA dataset...")
data_dir = snapshot_download(repo_id="gaia-benchmark/GAIA", repo_type="dataset")
dataset = load_dataset(data_dir, "2023_level1", split="validation")

# Convert to Pandas
df = dataset.to_pandas()

# Filter dataset (exclude multimedia tools and file uploads for this text-only agent)
# Conditions:
# A. Annotator Metadata does NOT contain video/image/youtube
# B. file_name is empty or null
mask_no_multimedia = ~df["Annotator Metadata"].astype(str).str.lower().str.contains("video|image|youtube", regex=True)
mask_no_file = df["file_name"].isnull() | (df["file_name"] == "")

filtered_df = df[mask_no_multimedia & mask_no_file].head(5).copy()

print(f"Loaded {len(filtered_df)} tasks for evaluation.")


# 2. Define Solver Wrapper
def query_solver_model(question):
    """
    Invokes the Deep Research Agent.
    """
    print(f"\n[Solver] Researching: {question[:50]}...")
    try:
        # invoke the graph with the question
        result = app.invoke({"topic": question})
        return result.get("final_report", "No report generated.")
    except Exception as e:
        return f"Error during research: {str(e)}"


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
# Import the ReAct agent
from lab_01_react import run_react_agent

# ... (Previous imports remain)

# 4. Run Evaluation Loop
results = []
for index, row in filtered_df.iterrows():
    task_id = row["task_id"]
    question = row["Question"]
    truth = row["Final answer"]
    metadata = str(row["Annotator Metadata"])

    print(f"\nProcessing Task: {task_id}")

    # --- Agent 1: Deep Research ---
    predicted_dr = query_solver_model(question)
    print(f"[Deep Research Output]: {predicted_dr[:100]}...")
    
    judge_resp_dr = query_judge_model(question, predicted_dr, truth, metadata)
    score_dr = extract_score(judge_resp_dr)
    print(f"Deep Research Score: {score_dr}")

    # --- Agent 2: ReAct Baseline ---
    print(f"[ReAct] Researching...")
    predicted_react = run_react_agent(question)
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
            "react_score": score_react
        }
    )


# 5. Summary
results_df = pd.DataFrame(results)
print("\n=== Evaluation Results ===")
print(results_df)

# Optional: Save to CSV
# results_df.to_csv("gaia_eval_results_pandas.csv", index=False)
