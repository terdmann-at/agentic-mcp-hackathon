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

# <solution>
# TODO: Implement this
pass
# </solution>

