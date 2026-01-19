import os

model = None

if "DATABRICKS_RUNTIME_VERSION" in os.environ:
    print("Running on Databricks.")
    from databricks_langchain import ChatDatabricks

    model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5", temperature=0)
else:
    print("Running locally.")

    import dotenv
    from langchain_openai.chat_models.azure import AzureChatOpenAI

    dotenv.load_dotenv()
    model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
