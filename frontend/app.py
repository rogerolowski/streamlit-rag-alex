import streamlit as st
from streamlit_chat import message
import requests

st.title("LEGO Price Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["is_user"], key=f"msg_{i}")

# Chat input
if prompt := st.chat_input("Ask about LEGO set prices..."):
    st.session_state.messages.append({"content": prompt, "is_user": True})
    message(prompt, is_user=True)

    # Send to FastAPI backend
    response = requests.post("http://backend:8000/chat", json={"query": prompt})
    if response.status_code == 200:
        bot_response = response.json()["response"]
        context = response.json().get("context", "")
        st.session_state.messages.append({"content": bot_response + f"\n(Context: {context})", "is_user": False})
        message(bot_response, key=f"bot_{len(st.session_state.messages)-1}")
    else:
        message("Error: Could not get response.", is_user=False)