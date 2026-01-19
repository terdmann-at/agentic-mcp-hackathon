import os

from databricks_langchain import ChatDatabricks
from databricks_langchain import DatabricksEmbeddings

model = None
embeddings = None
embedding_dimensions = 1536

if "DATABRICKS_RUNTIME_VERSION" in os.environ:
    print("Running on Databricks.")
    model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5", temperature=0)
    embeddings = DatabricksEmbeddings(endpoint="databricks-gte-large-en")
    embedding_dimensions = 1024
else:
    print("Running locally.")
    from langchain_openai.chat_models.azure import AzureChatOpenAI
    from langchain_openai import AzureOpenAIEmbeddings
    import dotenv
    dotenv.load_dotenv()
    model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
    embeddings = AzureOpenAIEmbeddings(deployment_name="text-embedding-ada-002")
    embedding_dimensions = 1536