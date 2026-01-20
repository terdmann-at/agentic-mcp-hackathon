# %% [markdown]
# # Building a Chatbot
#
# First, we'll need to install a couple packages. If using serverless, add the packages `langchain` and `databricks-langchain` to the environment.
# If not using serverless run the below cell.
#

# %%
# %pip install langchain databricks-langchain
# %restart_python

# %% [markdown]
# Today we'll be working with Databricks LLMs.
# Below we see an example for how to instantiate the model and for how
# to invoke it.

# %%
from databricks_langchain import ChatDatabricks
from langchain.messages import AIMessage, HumanMessage
from llm import model

response = model.invoke("hi")
print(response.content)


# %%
# Exercise 1: Console Chatbot
#
# Build a simple chatbot using langchain and the Chat Completions API.
#
# Fill in the lines inside <solution></solution>.
#


def chat_shell():
    # Initialize chat history
    chat_history: list[HumanMessage | AIMessage] = []

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Exercise 1.1: Add user message to the chat history.
        # <solution>
        chat_history.append(HumanMessage(content=user_input))
        # </solution>

        # Exercise 1.2: Invoke the model to get a response.
        # Hint: Use `model.invoke(...)`
        # <solution>
        response = model.invoke(chat_history)
        # </solution>
        print(f"AI: {response.content}")

        # Add AI message
        chat_history.append(response)


# %%
# Run the chatbot
chat_shell()

# %% [markdown]
# ## Exercise 2 (Bonus): Streamlit Chatbot
# Use streamlit to build a simple chat interface.
# Bonus points for using LangGraph.
#
# To test it, deploy the app.py to databricks apps using the UI.
#
# We'll need a couple files. That's why we create a directory first.
# Then we create a requirements.txt file, an app.yaml file and finally the app.py file. 
# The app.yaml file defines the command to run the app.py file.
# The requirements.txt file defines the dependencies.

# %%
# %mkdir streamlit_app_01

# %%
# %%writefile streamlit_app_01/requirements.txt
# databricks-langchain
# langchain
# streamlit

# %%
# %%writefile streamlit_app_01/app.yaml
# command: ["streamlit", "run", "app.py"]

# %%
# %%writefile streamlit_app_01/app.py
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

st.title("Chatbot")

# Exercise 2.1: Invoke the model with the message history
# <solution>
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
        st.markdown(message.content)

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5")
        response = model.invoke(st.session_state.messages)
        st.markdown(response.content)
        st.session_state.messages.append(response)
# </solution>
