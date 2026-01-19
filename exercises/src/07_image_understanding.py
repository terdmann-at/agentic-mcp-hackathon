# %% [markdown]
# # Image Understanding Chatbot
#
# First, we'll need to install a couple packages. If using serverless, add the packages `langchain` and `databricks-langchain` to the environment.
# If not using serverless run the below cell.
#

# %%
# %pip install langchain databricks-langchain
# %restart_python

# %% [markdown]
# Today we'll be working with Databricks LLMs that support vision capabilities.
# Below we see an example for how to instantiate the model and invoke it with an image.

# %%
import base64
import requests
from databricks_langchain import ChatDatabricks
from langchain_core.messages import HumanMessage, AIMessage

model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5")

# Helper to encode image from local path
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Example usage with a URL
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
response = model.invoke(
    [
        HumanMessage(
            content=[
                {"type": "text", "text": "Describe this image detailedly:"},
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                },
            ]
        )
    ]
)
print(response.content)

# %% [markdown]
# Now it's your turn. Solve the exercises below.
#
# To test your chatbot, run this on the terminal:
#

# %%
# %%
# Exercise 7.1:
#
# Build a simple chatbot that can understand images using langchain.
# The user should provide an image URL or path at the beginning.
#
# Fill in the lines inside <solution></solution>.
#

def chat_shell_vision():
    # Initialize chat history
    chat_history: list[HumanMessage | AIMessage] = []
    
    print("Welcome to the Vision Chatbot!")
    image_input = input("Please provide an image URL or local file path: ")

    start_message_content = []
    
    # Simple check if it's a URL or local file
    if image_input.startswith("http"):
        # <solution>
        start_message_content.append({"type": "image_url", "image_url": {"url": image_input}})
        # </solution>
    else:
        try:
            # <solution>
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
    start_message_content.insert(0, {"type": "text", "text": "I will ask you questions about this image."})
    chat_history.append(HumanMessage(content=start_message_content))
    
    # Get initial response/acknowledgement
    response = model.invoke(chat_history)
    print(f"AI: {response.content}")
    chat_history.append(response)

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Exercise 7.1.1: Add user message and invoke model
        # <solution>
        chat_history.append(HumanMessage(content=user_input))
        response = model.invoke(chat_history)
        print(f"AI: {response.content}")
        chat_history.append(response)
        # </solution>

# %%
# Run the chatbot
# chat_shell_vision()


# %%
# %% [markdown]
# ## Exercise 7.2 (Bonus):
# Use streamlit to build a chat interface with image upload.
#
# To test it, deploy the app.py to databricks apps using the UI.

# %%
# %mkdir streamlit_app_01_vision

# %%
# %%writefile streamlit_app_01_vision/requirements.txt
# databricks-langchain
# langchain
# streamlit

# %%
# %%writefile streamlit_app_01_vision/app.yaml
# command: ["streamlit", "run", "app.py"]

# %%
# %%writefile streamlit_app_01_vision/app.py
import streamlit as st
from databricks_langchain import ChatDatabricks
from langchain_core.messages import HumanMessage, AIMessage
import base64

st.title("Vision Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for image upload
with st.sidebar:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    image_url = st.text_input("Or enter Image URL")

# Handle image input
current_image_content = None
if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    current_image_content = {
        "type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
    }
elif image_url:
    st.image(image_url, caption="Image from URL", use_container_width=True)
    current_image_content = {
        "type": "image_url",
        "image_url": {"url": image_url}
    }

for message in st.session_state.messages:
    with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
        if isinstance(message.content, list):
             # Handle multimodal content display if needed, currently just showing text part if present?
             # For simplicity, we might just show the text part in the chat history for now
             for block in message.content:
                 if isinstance(block, dict) and block.get("type") == "text":
                     st.markdown(block["text"])
        else:
            st.markdown(message.content)

if prompt := st.chat_input("Ask something about the image"):
    
    # Construct message content
    message_content = []
    
    # If this is the FIRST message and we have an image, attach it
    # Ideally we'd want to attach it contextually, but simple approach:
    # If there are no previous messages, attach image. 
    # Or if the user just uploaded it. 
    # Let's attach it to the current message if it hasn't been "sent" yet.
    # A simple way to track if image is sent is to check history length or a flag.
    
    # Better approach for this demo: Always attach the image if present to *this* prompt 
    # to ensure the model sees it, or key off session state.
    # However, sending image every time consumes tokens. 
    # Let's send it only once at the start of conversation or if it changes (advanced).
    # Simple approach: If history is empty, attach image.
    
    has_image_in_history = any(
        isinstance(m, HumanMessage) and isinstance(m.content, list) and any(b.get("type") == "image_url" for b in m.content)
        for m in st.session_state.messages
    )
    
    if not has_image_in_history and current_image_content:
        message_content.append({"type": "text", "text": prompt})
        message_content.append(current_image_content)
    else:
        message_content = prompt # Just text

    st.session_state.messages.append(HumanMessage(content=message_content))
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        model = ChatDatabricks(endpoint="databricks-claude-sonnet-4-5")
        
        # Invoke model
        response = model.invoke(st.session_state.messages)
        
        st.markdown(response.content)
        st.session_state.messages.append(response)
# </solution>
