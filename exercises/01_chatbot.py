# %% [markdown]
# # Exercise 1: Chatbot
# 
# Goal: Build a simple chatbot using the Azure Chat Completions API.
# Expected time: 10 min


# %%
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

model = AzureChatOpenAI(
    deployment_name="gpt-4.1",
    temperature=0,
)

response = model.invoke("hi")
print(response.content)


# %% [markdown]
# ### Solution
# A continuous conversation loop.


# %%
from langchain_core.messages import HumanMessage, AIMessage

# Maintain chat history
chat_history = []

print("Chat with me! (Type 'exit' to quit)")
while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Add user message
    chat_history.append(HumanMessage(content=user_input))

    # Get response
    response = model.invoke(chat_history)
    print(f"AI: {response.content}")

    # Add AI message
    chat_history.append(response)

