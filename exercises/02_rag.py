# %% [markdown]
# # Exercise 2: RAG
#
# Goal: Implement a simple Retrieval Augmented Generation (RAG) system.
# Expected time: 10 min
#
# To test your RAG system, run this on the terminal:
#
#       uv run 02_rag.py
#

# %%
import glob
import os

from dotenv.main import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)

embed = AzureOpenAIEmbeddings(
    model="text-embedding-3-small",
    api_version=os.getenv("EMBED_API_VERSION"),
    azure_endpoint=os.getenv("EMBED_ENDPOINT"),
    api_key=os.getenv("EMBED_API_KEY"),
)


# %%
def create_vectorstore():
    pdf_folder = "data/knowledge_base"
    documents = []

    if not os.path.exists(pdf_folder):
        print(f"Warning: {pdf_folder} not found.")
        return None

    # Exercise 2.1: Load all PDFs from the folder
    for file in glob.glob(f"{pdf_folder}/*.pdf"):
        # <solution>
        loader = PyMuPDFLoader(file)
        documents.extend(loader.load())
        # </solution>

    if not documents:
        print("No documents found.")
        return None

    # Exercise 2.2: Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # <solution>
    splits = text_splitter.split_documents(documents)
    # </solution>

    # Exercise 2.3: Create vectorstore
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
