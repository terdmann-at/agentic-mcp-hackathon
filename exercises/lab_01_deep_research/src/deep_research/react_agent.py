from deep_research.react.graph import app


def run_react_agent(topic: str) -> str:
    """
    Runs the Manual ReAct agent on a topic.
    """
    print(f"--- Running Manual ReAct Agent on: {topic} ---")
    try:
        # LangGraph agents take 'messages' as input
        messages = [("user", topic)]

        # Invoke the graph
        # Note: 'app' here is the compiled graph from react/graph.py
        result = app.invoke({"messages": messages})

        # The result 'messages' list contains the conversation history
        # The last message is the AIMessage with the final answer
        final_message = result["messages"][-1]
        return final_message.content

    except Exception as e:
        return f"Error: {e}"
