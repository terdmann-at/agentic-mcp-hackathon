# %% [markdown]
# # Exercise 8: Reflexion Pattern
#
# Goal: Implement the **Reflexion** design pattern.
#
# Reflexion uses a "critique" step to verify the agent's output and provide feedback for a revision.
# This simple loop often improves performance on complex reasoning tasks significantly.
#
# Pattern: `Actor` -> `Evaluate/Critique` -> `Self-Reflection` -> `Repeat` (if needed).

# %%
from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0)

# %%
# 1. First Attempt Generation
# Let's give it a tricky task.

task_prompt = """
Write a python function that calculates the Levenshtein distance between two strings 
WITHOUT importing any libraries.
"""

# Initial Actor
actor = model
initial_solution = actor.invoke(task_prompt).content
print("--- Initial Solution ---")
print(initial_solution)

# %%
# 2. Critiques / Reflection
# Now we ask the model to critique its own code.

reflection_prompt = f"""
You are a senior software engineer. Review the following python code for correctness, efficiency, and style.
If there are errors, describe them clearly. If it is perfect, say "PERFECT".

Code:
{initial_solution}
"""

critique = model.invoke(reflection_prompt).content
print("\n--- Critique ---")
print(critique)

# %%
# 3. Revision
# We pass the original request, the initial solution, and the critique back to the actor.

if "PERFECT" not in critique:
    revision_prompt = f"""
    The user asked for: {task_prompt}

    You provided this solution:
    {initial_solution}

    The reviewer gave this feedback:
    {critique}

    Please rewrite the code to address the feedback.
    """

    final_solution = model.invoke(revision_prompt).content
    print("\n--- Final Solution ---")
    print(final_solution)
else:
    print("\nNo revision needed!")

# %% [markdown]
# ### Advanced Implementation
# In a real system (like using LangGraph), you would loop this cycle until the critique passed or a max_steps limit was reached.
# This technique is used in "Language Models can Solve Computer Tasks" (RCI) and many coding agents.
