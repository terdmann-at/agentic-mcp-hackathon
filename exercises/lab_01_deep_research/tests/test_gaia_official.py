import sys
import re
import string
from pathlib import Path
from dotenv import load_dotenv
from datasets import load_dataset
import pandas as pd

# Load env vars
load_dotenv()

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))
# sys.path.append(str(Path(__file__).parent.parent / "src"))

# Import Agents (Try User Impl first, then Solution)
try:
    from deep_research.mas.graph import mas_app as user_mas
except ImportError:
    user_mas = None

try:
    from solutions.mas.graph import mas_app as solution_mas
except ImportError:
    solution_mas = None

# Select which agent to test
mas_app = user_mas if user_mas else solution_mas
AGENT_NAME = "Student MAS" if user_mas else "Solution MAS"
if not mas_app:
    print("No MAS agent found (neither src nor solutions). Exiting.")
    sys.exit(1)

def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def check_is_correct(prediction, ground_truth):
    """Check if the ground truth is strictly included in the prediction."""
    norm_pred = normalize_answer(prediction)
    norm_gt = normalize_answer(ground_truth)
    return norm_gt in norm_pred

def run_evaluation(num_samples=3):
    print(f"\n=== GAIA Official Evaluation ({AGENT_NAME}) ===\n")
    print("Loading gaia-benchmark/GAIA (validation split)...")
    
    try:
        ds = load_dataset("gaia-benchmark/GAIA", "2023_all", split="validation")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # Take a small sample for speed
    examples = ds.select(range(num_samples))
    results = []

    # print(f"Dataset columns: {ds.column_names}")

    for ex in examples:
        question = ex["Question"]
        ground_truth = ex["Final Answer"] if "Final Answer" in ex else ex.get("Final answer", ex.get("final_answer", ""))
        level = ex["Level"]
        
        print(f"\n[Level {level}] Q: {question[:100]}...")
        
        # Run Agent
        initial_state = {
            "topic": question,
            "sub_topics": [],
            "research_outputs": [],
            "final_report": ""
        }
        
        try:
            output = mas_app.invoke(initial_state)
            prediction = output.get("final_report", "")
        except Exception as e:
            print(f"Agent failed: {e}")
            prediction = ""

        # Score
        is_correct = check_is_correct(prediction, ground_truth)
        status = "PASS" if is_correct else "FAIL"
        
        print(f"GT: {ground_truth}")
        print(f"Pred (concise): {prediction[:100]}...")
        print(f"Status: {status}")
        
        results.append({
            "Question": question[:50],
            "Level": level,
            "Ground Truth": ground_truth,
            "Passed": is_correct
        })

    # Summary Table
    df = pd.DataFrame(results)
    print("\n=== LEADERBOARD STYLE RESULTS ===\n")
    print(df.to_markdown(index=False))
    
    accuracy = df["Passed"].mean() * 100
    print(f"\nAccuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    run_evaluation()
