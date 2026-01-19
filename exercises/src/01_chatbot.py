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

model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5")

response = model.invoke("hi")
print(response.content)


# %% [markdown]
# Now it's your turn. Solve the exercises below.
#
# To test your chatbot, run this on the terminal:
#


# %%
# Exercise 1.1:
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

        # Exercise 1.2: Invoke th model to get a response.
        # <solution>
        response = model.invoke(chat_history)
        # </solution>
        print(f"AI: {response.content}")

        # Add AI message
        chat_history.append(response)


# %%
# Run the chatbot
chat_shell()


# %%
# %% [markdown]
# ## Exercise 1.2 (Bonus):
# Use streamlit to build a simple chat interface.
#
# To test it, deploy the app.py to databricks apps using the UI.

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
# <solution>
import streamlit as st
from databricks_langchain import ChatDatabricks

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message("user" if message is HumanMessage else "assistant"):
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
