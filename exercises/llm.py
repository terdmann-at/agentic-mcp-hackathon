import os

from databricks_langchain import ChatDatabricks
from langchain_openai.chat_models.azure import AzureChatOpenAI

model = None

if "DATABRICKS_RUNTIME_VERSION" in os.environ:
    print("Running on Databricks.")

    model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5", temperature=0)
else:
    print("Running locally.")

    import dotenv

    dotenv.load_dotenv()
    model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
