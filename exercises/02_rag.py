# %% [markdown]
# # Exercise 2: RAG
# 
# Goal: Implement a simple Retrieval Augmented Generation (RAG) system.
# Expected time: 10 min


# %%
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)


# %%
# Knowledge Base
documents = [
    "The workshop is about Agentic AI and MCP.",
    "The workshop date is 21.01.2026.",
    "The instructor is Tore Erdmann.",
    "RAG stands for Retrieval Augmented Generation."
]


# %%
def retrieve(query):
    # TODO: Implement a simple retrieval mechanism (e.g. keyword matching or just return all)
    matching_docs = [doc for doc in documents if any(word.lower() in doc.lower() for word in query.split())]
    return matching_docs if matching_docs else documents # Fallback to all for small valid set

query = "Who is the instructor?"
context = retrieve(query)
print(f"Context: {context}")


# %%
# Generate Answer
prompt = ChatPromptTemplate.from_template("Answer the question based on the context:\nContext: {context}\nQuestion: {question}")
chain = prompt | model

response = chain.invoke({"context": "\n".join(context), "question": query})
print(response.content)

