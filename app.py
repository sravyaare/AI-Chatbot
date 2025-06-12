import streamlit as st
import requests

# Title: Hugging Face API Configuration
API_TOKEN = "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"  # Replace with your actual Hugging Face token
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Title: Function to call Hugging Face Inference API
def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error("API Request Failed: " + str(e))
        return None

# Title: Streamlit App Configuration and Header
st.set_page_config(page_title="AI Chatbot")
st.title("Chatbot using Hugging Face API")
st.markdown("Start a conversation with the LLaMA 3.1-powered chatbot.")

# Title: Initialize Chat History
if "history" not in st.session_state:
    st.session_state.history = []

# Title: Input from User
user_input = st.text_input("Type your message below:")

# Title: When Send Button is Clicked
if st.button("Send") and user_input:
    # Constructing prompt in LLaMA-3 format
    prompt = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n" + user_input + "\n<|start_header_id|>assistant<|end_header_id|>\n"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "top_p": 0.95,
            "do_sample": True
        }
    }

    response = query(payload)

    if response and "generated_text" in response:
        bot_reply = response["generated_text"]
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", bot_reply))
    elif response and "error" in response:
        st.error("API Error: " + response["error"])
    else:
        st.warning("Unexpected response. Please try again.")

# Title: Display Chat History
st.subheader("Conversation History")
for speaker, message in reversed(st.session_state.history):
    st.markdown("**" + speaker + ":** " + message)
