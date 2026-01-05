import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Load env vars
load_dotenv()

# Ensure we can import from src
# sys.path.append(str(Path(__file__).parent.parent))
# sys.path.append(str(Path(__file__).parent.parent / "src"))
from deep_research.graph import app

# Initialize Evaluator Model
evaluator_llm = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)

def test_gaia_question():
    """
    Runs the agent against a specific GAIA question and evaluates the response.
    """
    
    # 1. The GAIA Question
    gaia_question = """
    Which of the fruits shown in the 2008 painting "Embroidery from Uzbekistan" were served as part of the October 1949 breakfast menu for the ocean liner that was later used as a floating prop for the film "The Last Voyage"? 
    Give the items as a comma-separated list, ordering them in clockwise order based on their arrangement in the painting starting from the 12 o'clock position. Use the plural form of each fruit.
    """
    
    # 2. Run the Agent
    print("\n\nRunning Agent on GAIA Question...")
    if app is None:
        print("Agent not implemented yet (app is None). Skipping test.")
        return

    initial_state = {
        "topic": gaia_question,
        "sub_queries": [],
        "search_results": [],
        "summary": "",
        "iteration": 0
    }
    
    result = app.invoke(initial_state)
    agent_answer = result["summary"]
    
    print(f"\n--- Agent Answer ---\n{agent_answer}\n")
    
    # 3. Evaluate the Answer
    # We use the LLM as a referee
    
    eval_prompt = f"""
    You are a strict Evaluator for the GAIA benchmark. verify if the following answer meets ALL the constraints of the question.

    Question: {gaia_question}

    Answer: {agent_answer}

    Checklist:
    1. Did it identify the painting "Embroidery from Uzbekistan" (by Lee Krasner / Pollock)?
    2. Did it identify the ocean liner from "The Last Voyage" (SS Ile de France)?
    3. Did it find the fruits from the Oct 1949 breakfast menu? (Grapefruits, Apples, Pears, Grapes...)
    4. Is the list comma-separated?
    5. Is the order clockwise from 12 o'clock?
    6. Are fruits in plural form?

    If the answer is correct and meets all formatting constraints, output 'PASS'.
    Otherwise, output 'FAIL' and explain why.
    """
    
    eval_response = evaluator_llm.invoke(eval_prompt).content
    print(f"--- Evaluation ---\n{eval_response}")
    
    # 4. Assert Success
    assert "PASS" in eval_response, f"Reflexion Eval Failed: {eval_response}"

if __name__ == "__main__":
    test_gaia_question()
