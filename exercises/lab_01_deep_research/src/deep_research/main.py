import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Add the project root to sys.path so imports work
# sys.path.append(str(Path(__file__).parent.parent))


# Import agents
try:
    from deep_research.mas.graph import mas_app
    from deep_research.react_agent import run_react_agent

except ImportError:
    mas_app = None
    run_react_agent = None

def main():
    print("Welcome to the Deep Research Helper!")
    print("-------------------------------------")
    print("This lab is structured into 4 exercises:")
    print("1. Define Agent State (src/state.py)")
    print("2. Define Tools (src/tools.py)")
    print("3. Define Nodes (src/nodes.py)")
    print("4. Build Graph (src/graph.py)")
    print("-------------------------------------")
    
    mode = input("Select Mode:\n[1] ReAct Baseline\n[2] Deep Research MAS (Exercise)\n> ").strip()
    
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("\nWhat would you like to research? ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        print(f"\nStarting research on: {user_input}")
        
        if mode == "1":
            if run_react_agent:
                print("Running ReAct Baseline...")
                res = run_react_agent(user_input)
                print(f"\nResult:\n{res}")
            else:
                print("Error: ReAct agent not found.")
                
        elif mode == "2":
            if mas_app is None:
                print("Error: MAS app is not implemented yet. Implementing exercises is required.")
                print("Check src/mas/state.py, src/mas/nodes.py, and src/mas/graph.py")
                continue

            # Run MAS
            initial_state = {
                "topic": user_input,
                "sub_topics": [],
                "research_outputs": [],
                "final_report": ""
            }
            config = {"configurable": {"thread_id": "1"}}
            
            try:
                final_state = mas_app.invoke(initial_state, config)
                print("\n=== FINAL REPORT ===\n")
                print(final_state.get("final_report", "No report generated."))
                print("\n====================")
            except Exception as e:
                print(f"Error: {e}")
                print("Did you implement the MAS exercises?")

def start_ui():
    """Entry point for the streamlit app."""
    import sys
    from streamlit.web import cli as stcli
    
    sys.argv = ["streamlit", "run", str(Path(__file__).parent / "streamlit_app.py")]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
