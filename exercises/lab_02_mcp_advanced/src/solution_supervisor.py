
import asyncio
import os
import operator
from typing import Annotated, Any, Dict, List, Literal, Sequence, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import create_react_agent
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools

# Local tools
from src.tools.web_search import visit_webpage

@tool
def web_search(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string."""
    return visit_webpage(url)

# Configuration
DOCKER_SERVER_SCRIPT = "src/mcp_server_docker.py"

# --- Supervisor Agent Definition ---

members = ["Researcher", "Coder"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)

options = ["FINISH"] + members

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str

async def main():
    # 1. Connect to Servers
    docker_server_params = StdioServerParameters(
        command="uv",
        args=["run", DOCKER_SERVER_SCRIPT],
        env=os.environ.copy(),
    )
    reasoning_server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
        env=os.environ.copy(),
    )
    
    print("Connecting to MCP servers...")
    
    async with stdio_client(docker_server_params) as (read_docker, write_docker), \
               stdio_client(reasoning_server_params) as (read_reasoning, write_reasoning):
        
        async with ClientSession(read_docker, write_docker) as session_docker, \
                   ClientSession(read_reasoning, write_reasoning) as session_reasoning:
            
            await session_docker.initialize()
            await session_reasoning.initialize()
            print("Connected.")

            # 2. Tools
            docker_tools = await load_mcp_tools(session_docker)
            reasoning_tools = await load_mcp_tools(session_reasoning)
            search_tools = [web_search]

            model = AzureChatOpenAI(deployment_name="gpt-4o", temperature=0)

            # 3. Create Agents
            
            # Researcher: Uses Web Search + Sequential Thinking
            researcher_agent = create_react_agent(
                model, 
                search_tools + reasoning_tools, 
                state_modifier="You are a researcher. Use sequential thinking to plan, and web search to find info."
            )
            
            # Coder: Uses Docker Execution
            coder_agent = create_react_agent(
                model, 
                docker_tools, 
                state_modifier="You are a creative coder. Use python execution to analyse data or create visualizations."
            )

            # 4. Define Nodes
            async def researcher_node(state: AgentState) -> dict:
                result = await researcher_agent.ainvoke(state)
                return {"messages": [HumanMessage(content=result["messages"][-1].content, name="Researcher")]}

            async def coder_node(state: AgentState) -> dict:
                result = await coder_agent.ainvoke(state)
                return {"messages": [HumanMessage(content=result["messages"][-1].content, name="Coder")]}

            # Supervisor Node
            class Router(TypedDict):
                next: Literal["Researcher", "Coder", "FINISH"]

            supervisor_prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next?"
                    " Or should we FINISH? Select one of: {options}",
                ),
            ]).partial(options=str(options), members=", ".join(members))
            
            supervisor_chain = supervisor_prompt | model.with_structured_output(Router)

            async def supervisor_node(state: AgentState) -> dict:
                result = await supervisor_chain.ainvoke(state)
                return {"next": result["next"]}

            # 5. Build Graph
            workflow = StateGraph(AgentState)
            workflow.add_node("Supervisor", supervisor_node)
            workflow.add_node("Researcher", researcher_node)
            workflow.add_node("Coder", coder_node)

            workflow.add_edge(START, "Supervisor")
            
            workflow.add_conditional_edges("Supervisor", lambda x: x["next"], {
                "Researcher": "Researcher",
                "Coder": "Coder",
                "FINISH": END
            })
            
            workflow.add_edge("Researcher", "Supervisor")
            workflow.add_edge("Coder", "Supervisor")

            app = workflow.compile()

            # 6. Run
            print("\n" + "="*50)
            print("Supervisor Agent Ready. Enter request (e.g. 'Research X and plot Y').")
            print("="*50 + "\n")

            while True:
                user_input = input("User: ")
                if user_input.lower() in ["q", "quit", "exit"]:
                    break
                
                async for chunk in app.astream(
                    {"messages": [HumanMessage(content=user_input)]},
                    stream_mode="updates"
                ):
                    for node, values in chunk.items():
                        if "messages" in values:
                            print(f"\n--- {node} ---")
                            print(values["messages"][-1].content)
                        elif "next" in values:
                            print(f"\n--- Supervisor: Next -> {values['next']} ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Goodbye")
