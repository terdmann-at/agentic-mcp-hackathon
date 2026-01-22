import os

model = None
embeddings = None
embedding_dimensions = 1536

if "DATABRICKS_RUNTIME_VERSION" in os.environ:
    print("Running on Databricks.")
    from databricks_langchain import ChatDatabricks, DatabricksEmbeddings

    model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5", temperature=0)
    embeddings = DatabricksEmbeddings(endpoint="databricks-gte-large-en")
    embedding_dimensions = 1024
else:
    print("Running locally.")
    import dotenv
    from langchain_openai import AzureOpenAIEmbeddings
    from langchain_openai.chat_models.azure import AzureChatOpenAI

    dotenv.load_dotenv()
    model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
    embeddings = AzureOpenAIEmbeddings(endpoint="text-embedding-003-large")
    embedding_dimensions = 1536
