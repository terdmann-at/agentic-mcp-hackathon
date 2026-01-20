# %% [markdown]
# # Exercise 2: RAG
#
# Goal: Implement a simple Retrieval Augmented Generation (RAG) system.
#

# %%
# %pip install databricks-langchain langchain-community pymupdf
# %restart_python

# %%
import glob
import os

from databricks_langchain import ChatDatabricks, DatabricksEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# %%
model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5")
embed = DatabricksEmbeddings(endpoint="databricks-gte-large-en")


# %%
def create_vectorstore():
    pdf_folder = "data/knowledge_base"
    documents = []

    if not os.path.exists(pdf_folder):
        print(f"Warning: {pdf_folder} not found.")
        return None

    # Exercise 2.1: Load all PDFs from the folder
    # Hint: Use `PyMuPDFLoader(file).load()`
    for file in glob.glob(f"{pdf_folder}/*.pdf"):
        # <solution>
        loader = PyMuPDFLoader(file)
        documents.extend(loader.load())
        # </solution>

    if not documents:
        print("No documents found.")
        return None

    # Exercise 2.2: Split documents
    # Hint: Use `RecursiveCharacterTextSplitter`
    # <solution>
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    # </solution>

    # Exercise 2.3: Create vectorstore.
    # Hint: Use the `InMemoryVectorStore` constructor.
    # <solution>
    vectorstore = InMemoryVectorStore.from_documents(
        documents=splits,
        embedding=embed,
    )
    # </solution>
    return vectorstore


# %%
def retrieve(vectorstore, query: str):
    # Exercise 2.4: Implement a retriever using the vectorstore.
    # <solution>
    retriever = vectorstore.as_retriever()
    matching_docs = retriever.invoke(query)
    # </solution>
    return [doc.page_content for doc in matching_docs]


# %%
def main():
    # Initialize
    vectorstore = create_vectorstore()
    if not vectorstore:
        return

    query = "What surface additives have excellent leveling properties?"
    context = retrieve(vectorstore, query)

    # Exercise 2.5: Generate Answer
    prompt = ChatPromptTemplate.from_template(
        "Answer the question based on the context:\nContext: {context}\nQuestion: {question}"
    )
    # <solution>
    chain = prompt | model
    response = chain.invoke({"context": "\n".join(context), "question": query})
    # </solution>
    print(f"Question: {query}")
    print(f"Answer: {response.content}")


if __name__ == "__main__":
    main()
    # Response should include: BYK-388, BYK-3440, and BYK-3441
