import streamlit as st
import requests  

# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000/chat"

# Set page title
st.set_page_config(page_title="💬 IT Support Chatbot", layout="wide")

# Customizing UI
st.title("💬 IT Support Chatbot")
st.markdown("Ask me about IT issues, and I'll try to help you! 😊")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input field
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Send request to FastAPI chatbot
    response = requests.get(API_URL, params={"query": user_input}).json()
    bot_response = response["response"]

    # Display bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.chat_message("assistant").write(bot_response)
