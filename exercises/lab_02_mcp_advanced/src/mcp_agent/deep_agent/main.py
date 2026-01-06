import asyncio
import mlflow
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from .graph import graph
from .fs_tools import SANDBOX_ROOT


async def amain():
    load_dotenv()

    # Initialize MLflow
    mlflow.set_experiment("MCP Deep Agent")
    mlflow.langchain.autolog()

    print("=" * 50)
    print("Deep Research Agent")
    print("Capabilities: Planning, Filesystem, Sub-agents")
    print(f"Sandbox: {SANDBOX_ROOT}")
    print("=" * 50 + "\n")

    # Initial state
    thread_id = "1"
    config = {"recursion_limit": 50, "configurable": {"thread_id": thread_id}}

    with mlflow.start_span(name="Deep Agent Conversation"):
        while True:
            try:
                # Check for pending interruptions
                snapshot = await graph.aget_state(config)
                
                if snapshot.next and "tools" in snapshot.next:
                    # We are interrupted before tool execution
                    last_msg = snapshot.values["messages"][-1]
                    print("\n" + "!" * 50)
                    print("INTERRUPTION: Pending Tool Call(s)")
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        for tc in last_msg.tool_calls:
                             print(f"  -> {tc['name']}({tc['args']})")
                    print("!" * 50 + "\n")
                    
                    user_input = input("Approve tool execution? (y/n/reason): ")
                    if user_input.lower() in ["y", "yes"]:
                        print("Resuming execution...")
                        inputs = None
                    elif user_input.lower() in ["n", "no"]:
                         print("Aborting tool call. Providing feedback...")
                         # To abort, we can provide a tool error or a user message. 
                         # For simplicity, let's treat it as feedback instructions.
                         inputs = HumanMessage(content="I do not approve this tool call. Please stop or try a different approach.")
                    elif user_input.lower() in ["q", "quit", "exit"]:
                        break
                    else:
                        # Treat as feedback/modification
                        inputs = HumanMessage(content=user_input)

                else:
                    # Normal start of turn
                    user_input = input("User: ")
                    if user_input.lower() in ["q", "quit", "exit"]:
                        break
                    
                    inputs = {"messages": [HumanMessage(content=user_input)]}

                # Stream the execution
                async for event in graph.astream(
                    inputs, config=config, stream_mode="updates"
                ):
                    for node, updates in event.items():
                        if "messages" in updates:
                            last_msg = updates["messages"][-1]
                            print(
                                f"[{node}]: {last_msg.content[:100]}..."
                                if last_msg.content
                                else f"[{node}]: Tool Call"
                            )

                            if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                                for tc in last_msg.tool_calls:
                                    print(f"  -> Calling {tc['name']} with {tc['args']}")

                        if "todos" in updates:
                            print(f"[{node}]: Update Logic - Todos updated.")
                            for t in updates["todos"]:
                                status_icon = "[x]" if t["status"] == "completed" else "[ ]"
                                print(f"  {status_icon} {t['task']}")

                print("\n" + "-" * 30 + "\n")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    asyncio.run(amain())


if __name__ == "__main__":
    main()
