import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Add the project root to sys.path so imports work
sys.path.append(str(Path(__file__).parent.parent))

from src.graph import app

def main():
    print("Welcome to the Deep Research Helper!")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("\nWhat would you like to research? ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        print(f"\nStarting research on: {user_input}")
        
        # Initialize with just the topic, everything else empty
        initial_state = {
            "topic": user_input,
            "sub_queries": [],
            "search_results": [],
            "summary": "",
            "iteration": 0
        }
        
        # Run the graph
        # Providing a thread_id enables memory (if we add a checkpointer later)
        config = {"configurable": {"thread_id": "1"}}
        
        try:
            # We invoke the app and get the final state back
            final_state = app.invoke(initial_state, config)
            
            print("\n=== FINAL REPORT ===\n")
            print(final_state["summary"])
            print("\n====================")
            
        except Exception as e:
            print(f"Error: {e}")
            print("Did you implement all the exercises?")
            print("Check src/state.py, src/tools.py, src/nodes.py, and src/graph.py")

if __name__ == "__main__":
    main()
