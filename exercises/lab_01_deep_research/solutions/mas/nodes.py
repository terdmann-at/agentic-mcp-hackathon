from langchain_openai import AzureChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from solutions.mas.state import ResearchState, ResearchPlan, SubTaskState

# Initialize Model
llm = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
search_tool = DuckDuckGoSearchRun()

def chief_editor_node(state: ResearchState):
    """
    The 'Manager': Breaks the user's topic into sub-topics for parallel research.
    """
    print(f"--- [Chief Editor] Planning: {state['topic']} ---")
    
    planner = llm.with_structured_output(ResearchPlan)
    prompt = (
        f"You are a Research Manager. Your goal is to break down the following research topic into 3 distinct, "
        f"targeted sub-topics that will convince a search engine to reveal specific facts, numbers, or data points.\n\n"
        f"Topic: {state['topic']}\n\n"
        f"Return 3 to 5 distinct sub-topics."
    )
    plan = planner.invoke(prompt)
    
    return {"sub_topics": plan.sub_topics}

def research_worker_node(state: SubTaskState):
    """
    The 'Worker': Takes a single sub-topic, searches, and returns the result.
    Note: The input is SubTaskState, not ResearchState.
    """
    topic = state["topic"]
    print(f"--- [Worker] Searching for: {topic} ---")
    
    # Simple tool call
    try:
        res = search_tool.invoke(topic)
    except Exception as e:
        res = f"Search failed: {e}"
        
    return {"research_outputs": [f"## Subtopic: {topic}\n{res}\n"]}

def writer_node(state: ResearchState):
    """
    The 'Writer': Compiles all research outputs into a final report.
    """
    print("--- [Writer] Compiling Report ---")
    
    # Join all collected results
    # formatting depends on how Send returns data, usually it's a list in 'research_outputs'
    combined_content = "\n\n".join(state["research_outputs"])
    
    prompt = f"""
    You are a technical writer. Compile the following research notes into a comprehensive final report.
    
    Topic: {state['topic']}
    
    Research Notes:
    {combined_content}
    
    Instructions:
    1. Synthesize the information into a clear, well-structured report.
    2. If the original topic asked for a specific format (e.g. list, number, zip code), ensure you explicitly provide it.
    3. MANDATORY: You MUST end the report with a section labeled exactly "Final Answer:" containing the specific answer to the user's question, without extra commentary.
    
    Report:
    """
    
    response = llm.invoke(prompt)
    return {"final_report": response.content}
