# --- Exercise 3: Define Nodes ---
# Goal: Implement the logic for each step in the research workflow.

from langchain_openai import AzureChatOpenAI
from src.state import ResearchState, ResearchPlan
from src.tools import search_tool

# Initialize the Model
# Adjust deployment_name if needed
llm = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)

def planner_node(state: ResearchState):
    """
    1. Identify the topic from the state.
    2. Use the LLM to generate a plan (3 structured sub-queries).
    3. Return the new 'sub_queries' list to update the state.
    """
    print(f"--- PLANNING: {state['topic']} ---")
    
    # We enforce structured output to ensure we get a list of strings
    planner = llm.with_structured_output(ResearchPlan)
    
    prompt = f"Generate 3 distinct search queries to gather comprehensive information about: {state['topic']}"
    plan = planner.invoke(prompt)
    
    return {"sub_queries": plan.items}

def searcher_node(state: ResearchState):
    """
    1. Read 'sub_queries' from state.
    2. For each query, execute the search_tool. 
    3. Return 'search_results' (which will be appended to the state list).
    """
    print("--- SEARCHING ---")
    queries = state["sub_queries"]
    results = []
    
    for q in queries:
        print(f"Searching for: {q}")
        # In a real app, you might want error handling here
        res = search_tool.invoke(q)
        results.append(f"Query: {q}\nResult: {res}\n")
        
    return {"search_results": results}

def synthesizer_node(state: ResearchState):
    """
    1. Read accumulated 'search_results' from state.
    2. Ask the LLM to write a final report based on these results.
    3. Return 'summary'.
    """
    print("--- SYNTHESIZING ---")
    
    results = "\n\n".join(state["search_results"])
    
    prompt = f"""
    You are a research assistant. 
    Basd on the following search results, write a comprehensive answer to the request: '{state['topic']}'.
    
    Search Results:
    {results}
    
    Answer:
    """
    
    response = llm.invoke(prompt)
    
    return {"summary": response.content}
