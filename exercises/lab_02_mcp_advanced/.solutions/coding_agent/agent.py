from langchain.agents import create_agent


def build_agent(model, tools):
    # <solution>
    system_message = """You are an advanced autonomous research assistance.
    You have access to the following capabilities:
    1. **Sequential Thinking**: Use this to plan your approach and breakdown complex problems. 
       ALWAYS start by using this tool to plan your steps.
    2. **Docker Code Execution**: You can execute Python code in a safe sandboxed environment. 
       Use this for calculations, data analysis, or verifying code logic. 
       ALWAYS use code execution for math. Do not calculate mentally.
       IMPORTANT: Variables must be printed to be seen (e.g. `print(result)`). The system does not auto-print the last expression.
       The environment has pandas and matplotlib installed.
    3. **Web Search**: You can visit webpages to gather information.
    
    Solve the user's request by combining these tools. 
    """

    return create_agent(model, tools, system_prompt=system_message)
    # </solution>
