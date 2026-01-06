# test_react.py
from dotenv import load_dotenv

load_dotenv()

from deep_research.react.graph import app  # noqa: E402
from langchain_core.messages import HumanMessage  # noqa: E402


def test():
    print("Testing Manual ReAct Agent...")
    msg = HumanMessage(content="What is the capital of France?")
    result = app.invoke({"messages": [msg]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    test()
