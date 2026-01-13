# %% [markdown]
# # Exercise 9: GAIA Question with Reflexion
#
# Goal: Solve a hard GAIA benchmark question using a Reflexion (ReAct + Critique) loop.
#
# GAIA Question:
# "Which of the fruits shown in the 2008 painting 'Embroidery from Uzbekistan' were served
# as part of the October 1949 breakfast menu for the ocean liner that was later used as a
# floating prop for the film 'The Last Voyage'? Give the items as a comma-separated list..."
#
# This requires:
# 1. Understanding the question (Multi-hop reasoning).
# 2. Tool use (Search) to find the painting and the ship's menu.
# 3. Critique/Reflexion to ensure all constraints are met (e.g., "plural form", "comma-separated").

# %%
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import AzureChatOpenAI

# 1. Setup Wrapper for easier handling
# We'll use a simple Agent wrapper to run the search
model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)
search_tool = DuckDuckGoSearchRun()
tools = [search_tool]

prompt = hub.pull("hwchase17/react")
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# %%
# 2. The GAIA Question
gaia_question = """
Which of the fruits shown in the 2008 painting "Embroidery from Uzbekistan" were served as part of the October 1949 breakfast menu for the ocean liner that was later used as a floating prop for the film "The Last Voyage"? 
Give the items as a comma-separated list, ordering them in clockwise order based on their arrangement in the painting starting from the 12 o'clock position. Use the plural form of each fruit.
"""

print(f"--- GAIA Question ---\n{gaia_question}\n")

# %%
# 3. First Attempt (Actor)
print("--- Attempt 1: Researching ---")
# We start with a plan or just run the agent.
try:
    initial_response = agent_executor.invoke({"input": gaia_question})
    initial_answer = initial_response["output"]
except Exception as e:
    initial_answer = f"Error during execution: {e}"

print(f"\nInitial Answer:\n{initial_answer}")

# %%
# <solution>
# 4. Critique (Reflector)
# usage: Criticize the answer based on the requirements.
critique_prompt = f"""
You are a strict Evaluator. Verify if the following answer meets ALL the constraints of the question.

Question: {gaia_question}

Answer: {initial_answer}

Checklist:
1. Did it identify the painting "Embroidery from Uzbekistan"?
2. Did it identify the ocean liner from "The Last Voyage"?
3. Did it find the Oct 1949 breakfast menu?
4. Is the list comma-separated?
5. Is the order clockwise from 12 o'clock?
6. Are fruits in plural form?

Output your critique. If it is perfect, end with "STATUS: PASS". If not, provide specific instructions to fix it and end with "STATUS: FAIL".
"""

critic_response = model.invoke(critique_prompt).content
print(f"\n--- Critique ---\n{critic_response}")

# 5. Iterative Improvement (Loop)
# If failed, we feed the critique back to the agent as "Context" to try again.

if "STATUS: FAIL" in critic_response:
    print("\n--- Attempt 2: Refining based on critique ---")

    # We construct a new prompt for the agent including the history
    retry_prompt = f"""
    Previous Attempt Answer: {initial_answer}
    
    Critique of Previous Attempt:
    {critic_response}
    
    Please try again to answer the original question, fixing the issues mentioned above.
    Original Question: {gaia_question}
    """

    final_response = agent_executor.invoke({"input": retry_prompt})
    final_answer = final_response["output"]
    print(f"\nFinal Answer:\n{final_answer}")
# </solution>

else:
    print("\nFirst attempt passed!")

# %% [markdown]
# ### Why this matters for GAIA
# GAIA questions result in low success rates (originally ~7% for GPT-4) because they are brittle.
# One missed step (e.g. wrong singular/plural form, wrong order) fails the question.
# Reflexion loops catch these "silly" errors by strictly validating against the constraints before submitting.
