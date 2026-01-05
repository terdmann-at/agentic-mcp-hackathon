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
    
    # Exercise: Implement the Chief Editor
    # Use the LLM to generate a 'ResearchPlan' from the topic.
    # The plan should contain 3-5 distinct sub-topics.
    # Return the sub_topics list.
    # <solution>
    # TODO: Implement this
    pass
    # </solution>

def research_worker_node(state: SubTaskState):
    """
    The 'Worker': Takes a single sub-topic, searches, and returns the result.
    Note: The input is SubTaskState, not ResearchState.
    """
    topic = state["topic"]
    print(f"--- [Worker] Searching for: {topic} ---")
    
    # Exercise: Implement the Research Worker
    # 1. Extract the 'topic' from the state.
    # 2. Use the 'search_tool' to find information.
    # 3. Handle potential tool errors gracefully.
    # 4. Return a key 'research_outputs' containing a list with the formatted result.
    # <solution>
    # TODO: Implement this
    pass
    # </solution>

def writer_node(state: ResearchState):
    """
    The 'Writer': Compiles all research outputs into a final report.
    """
    print("--- [Writer] Compiling Report ---")
    
    # Exercise: Implement the Writer
    # 1. Combine all 'research_outputs' from the state.
    # 2. Prompt the generic LLM (not structured) to write a final report.
    # 3. Ensure the prompt enforces a 'Final Answer:' section.
    # 4. Return the 'final_report'.
    # <solution>
    # TODO: Implement this
    pass
    # </solution>
