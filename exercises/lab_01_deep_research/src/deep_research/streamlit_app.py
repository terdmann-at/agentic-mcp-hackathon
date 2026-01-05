import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Add project root to sys.path
# sys.path.append(str(Path(__file__).parent.parent))


# Import agents
try:
    from deep_research.mas.graph import mas_app
    from deep_research.react_agent import run_react_agent

except ImportError:
    mas_app = None
    run_react_agent = None

st.set_page_config(page_title="Deep Research AI", page_icon="🔍")

st.title("🔍 Deep Research AI")

# Sidebar for mode selection
mode = st.sidebar.radio("Select Agent Mode:", ["ReAct Baseline", "Deep Research MAS"])

st.markdown(f"**Current Mode:** {mode}")

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
        with st.spinner("Researching..."):
            try:
                response = ""
                if mode == "ReAct Baseline":
                    if run_react_agent:
                        response = run_react_agent(prompt)
                    else:
                        st.error("ReAct Agent not implemented/found.")
                else:
                    # MAS Mode
                    if mas_app is None:
                        st.error("MAS app is not implemented yet. Please complete the exercises.")
                        st.info("Check src/mas/state.py, src/mas/nodes.py, and src/mas/graph.py")
                    else:
                        initial_state = {
                            "topic": prompt,
                            "sub_topics": [],
                            "research_outputs": [],
                            "final_report": ""
                        }
                        result = mas_app.invoke(initial_state)
                        response = result.get("final_report", "No report generated.")

                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
