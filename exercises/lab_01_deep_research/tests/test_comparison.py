import time
import pytest
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Load env vars
load_dotenv()

import sys
from pathlib import Path
# Add project root to sys.path
# Add project root and src to sys.path
# sys.path.append(str(Path(__file__).parent.parent))
# sys.path.append(str(Path(__file__).parent.parent / "src"))

from deep_research.react_agent import run_react_agent
try:
    from deep_research.mas.graph import mas_app
except ImportError:
    mas_app = None

# Evaluator
evaluator_llm = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)

def evaluate_answer(answer: str, question: str) -> str:
    """Uses LLM to grade the answer (PASS/FAIL)."""
    eval_prompt = f"""
    You are a strict Evaluator. Verify if the answering meets the requirements.
    
    Question: {question}
    Answer: {answer}
    
    If it is correct and detailed, output 'PASS'.
    If it is incorrect or misses key constraints, output 'FAIL'.
    """
    return evaluator_llm.invoke(eval_prompt).content

def run_mas_agent(topic: str) -> str:
    """Runs the Multi-Agent System."""
    print(f"--- Running MAS on: {topic} ---")
    initial_state = {
        "topic": topic,
        "sub_topics": [],
        "research_outputs": [],
        "final_report": ""
    }
    # Invoke
    result = mas_app.invoke(initial_state)
    return result["final_report"]

def test_comparison():
    """Compares ReAct vs MAS."""
    
    # 1. The GAIA Question
    gaia_question = """
    Which of the fruits shown in the 2008 painting "Embroidery from Uzbekistan" were served as part of the October 1949 breakfast menu for the ocean liner that was later used as a floating prop for the film "The Last Voyage"? 
    Give the items as a comma-separated list, ordering them in clockwise order based on their arrangement in the painting starting from the 12 o'clock position. Use the plural form of each fruit.
    """
    
    print("\n\n=== STARTING COMPARISON ===\n")
    
    # --- Run ReAct ---
    start_time = time.time()
    react_answer = run_react_agent(gaia_question)
    react_time = time.time() - start_time
    react_score = evaluate_answer(react_answer, gaia_question)
    print(f"\n[ReAct] Time: {react_time:.2f}s | Score: {react_score}")
    
    # --- Run MAS ---
    if mas_app is None:
        print("\n[MAS] Not implemented yet (mas_app is None). Skipping.")
        mas_time = 0
        mas_score = "N/A"
    else:
        start_time = time.time()
        mas_answer = run_mas_agent(gaia_question)
        mas_time = time.time() - start_time
        mas_score = evaluate_answer(mas_answer, gaia_question)
        print(f"\n[MAS] Time: {mas_time:.2f}s | Score: {mas_score}")
    
    print("\n=== RESULTS ===\n")
    print(f"| Agent | Time (s) | Result |")
    print(f"|-------|----------|--------|")
    print(f"| ReAct | {react_time:.2f}     | {react_score} |")
    print(f"| MAS   | {mas_time}     | {mas_score} |")
    
    # Soft assertion
    assert "PASS" in react_score or "FAIL" in react_score
    if mas_app:
        assert "PASS" in mas_score or "FAIL" in mas_score

if __name__ == "__main__":
    test_comparison()
