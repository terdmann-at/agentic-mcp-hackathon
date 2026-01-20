# %% [markdown]
# # Exercise 8: Image Understanding
#
# First, we'll need to install a couple packages. If using serverless, add the packages `langchain` and `databricks-langchain` to the environment.
# If not using serverless run the below cell.
#

# %%
# %pip install langchain databricks-langchain
# %restart_python

# %% [markdown]
# We'll be working with Databricks LLMs that support vision capabilities.
# Below we see an example for how to instantiate the model and invoke it with an image.

# %%
import base64
import urllib.request

from databricks_langchain import ChatDatabricks
from langchain_core.messages import AIMessage, HumanMessage

model = ChatDatabricks(endpoint="databricks-gemma-3-12b")

# Helper to encode image from local path
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Helper to encode image from URL
def encode_image_from_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        return base64.b64encode(response.read()).decode("utf-8")


# Example usage with a URL
image_url = "https://raw.githubusercontent.com/pytorch/vision/main/gallery/assets/dog1.jpg"
image_data = encode_image_from_url(image_url)

response = model.invoke(
    [
        HumanMessage(
            content=[
                {"type": "text", "text": "Describe this image detailedly:"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                },
            ]
        )
    ]
)
print(response.content)


# %%
# Exercise 8.1:
#
# Build a simple chatbot that can understand images using langchain.
# The user should provide an image URL or path at the beginning.
#

def chat_shell_vision():
    # Initialize chat history
    chat_history: list[HumanMessage | AIMessage] = []

    print("Welcome to the Vision Chatbot!")
    image_input = input("Please provide an image URL or local file path: ")

    start_message_content = []

    try:
        # Exercise 8.1.1: Request processing of the image
        # <solution>
        if image_input.startswith("http"):
             base64_image = encode_image_from_url(image_input)
        else:
             base64_image = encode_image(image_input)

        start_message_content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            }
        )
        # </solution>
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Add initial instruction
    start_message_content.insert(
        0, {"type": "text", "text": "I will ask you questions about this image."}
    )
    chat_history.append(HumanMessage(content=start_message_content))

    # Get initial response/acknowledgement
    response = model.invoke(chat_history)
    print(f"AI: {response.content}")
    chat_history.append(response)

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Exercise 8.1.3: Add user message and invoke model
        # <solution>
        chat_history.append(HumanMessage(content=user_input))
        response = model.invoke(chat_history)
        print(f"AI: {response.content}")
        chat_history.append(response)
        # </solution>


# %%
# Run the chatbot
chat_shell_vision()
