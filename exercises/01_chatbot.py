# %% [markdown]
# # Building a Chatbot
#
# Today we'll be working with GPT-4.1, deployed on Azure AI Foundry.
# Below we see an example for how to instantiate the model and for how
# to invoke it.

# %%

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    api_key=dbutils.notebook.entry_point.getDbutils()  # pyrefly: ignore
    .notebook()
    .getContext()
    .apiToken()
    .get(),
    base_url="https://adb-4139373877782449.9.azuredatabricks.net/serving-endpoints",
    model="o3-playground",
    temperature=1,
)

response = model.invoke("hi")
print(response.content)


# %% [markdown]
#
# Now it's your turn. Solve the exercises below.
#
# To test your chatbot, run this on the terminal:
#
#       uv run 01_chatbot.py
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


if __name__ == "__main__":
    chat_shell()


# %%
# Exercise 1.2 (Bonus):
#
# Use streamlit to build a simple chat interface.
#
#
# <solution>
# TODO: your code here
# </solution>
