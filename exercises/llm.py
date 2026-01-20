import os

from databricks_langchain import ChatDatabricks, DatabricksEmbeddings

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
    import dotenv
    from langchain_openai import AzureOpenAIEmbeddings
    from langchain_openai.chat_models.azure import AzureChatOpenAI

    dotenv.load_dotenv("exercises/.env")
    model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
    embeddings = AzureOpenAIEmbeddings(deployment_name="text-embedding-ada-002")
    embedding_dimensions = 1536

    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.graph import START, MessagesState, StateGraph

    graph = (
        StateGraph(MessagesState)
        .add_node(
            "chatbot", lambda state: {"messages": model.invoke(state["messages"])}
        )
        .add_edge(START, "chatbot")
        .compile(checkpointer=MemorySaver())
    )
    config = {"configurable": {"thread_id": "1"}}
    while True:
        user_input = input("User: ")
        response = graph.invoke({"messages": [("user", user_input)]}, config)
        print(f"AI: {response['messages'][-1].content}")


from langgraph.checkpoint.memory import MemorySaver
from langgraph.func import entrypoint


@entrypoint(checkpointer=MemorySaver())
def chat_workflow(new_message: str, previous: list = None):
    history: list[HumanMessage | AIMessage] = previous or []
    # 1. Update history
    history.append(("user", new_message))
    # 2. Invoke model
    response = model.invoke(history)
    history.append(("assistant", response.content))
    return history


config = {"configurable": {"thread_id": "func_test_3"}}
while True:
    user_input = input("User: ")
    output = chat_workflow.invoke(user_input, config=config)
    print("AI: ", output[-1][1])

