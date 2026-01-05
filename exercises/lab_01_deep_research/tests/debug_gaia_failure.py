import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from solutions.mas.graph import mas_app

def debug_failure():
    # Question that failed: Zip code of invasive fish
    question = "I’m researching species that became invasive after people who kept them as pets released them. There’s a certain species of fish that was popularized as a pet by being the main character of the movie Finding Nemo. According to the USGS, where was this fish found as a nonnative species, before the year 2020? I need the answer formatted as the five-digit zip codes of the places the species was found, separated by commas if there is more than one place."
    
    gt = "34689"
    
    print(f"--- Running Debug on: {question[:50]}... ---")
    
    initial_state = {
        "topic": question,
        "sub_topics": [],
        "research_outputs": [],
        "final_report": ""
    }
    
    try:
        result = mas_app.invoke(initial_state)
        report = result.get("final_report", "")
        
        print("\n=== FULL REPORT ===\n")
        print(report)
        print("\n===================\n")
        
        if gt in report:
            print(f"SUCCESS: GT '{gt}' found in report.")
        else:
            print(f"FAILURE: GT '{gt}' NOT found in report.")
            
    except Exception as e:
        print(f"Error: {e}")

def analyze_dataset():
    from datasets import load_dataset
    print("Loading dataset for analysis...")
    ds = load_dataset("gaia-benchmark/GAIA", "2023_all", split="validation")
    print("\n=== DATASET EXAMPLE ROW ===")
    row = ds[0]
    for k, v in row.items():
        print(f"{k}: {v}")
    print("===========================\n")

if __name__ == "__main__":
    analyze_dataset()
    # debug_failure()
