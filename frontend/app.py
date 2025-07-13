import streamlit as st
from streamlit_chat import message
import requests
import json

# Page config
st.set_page_config(
    page_title="LEGO Price Assistant",
    page_icon="🧱",
    layout="wide"
)

st.title("🧱 LEGO Price Assistant")
st.markdown("Ask me about LEGO set prices and values!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar with examples and info
with st.sidebar:
    st.header("💡 Example Questions")
    st.markdown("""
    Try asking:
    - "What's the price of set 75192?"
    - "How much does the Millennium Falcon cost?"
    - "Price of 10179-1"
    - "Value of Hogwarts Castle 71043"
    """)
    
    st.header("ℹ️ How it works")
    st.markdown("""
    1. Ask about any LEGO set price
    2. I'll look up the set details
    3. Get an AI-powered price estimate
    4. Consider factors like rarity, age, and pieces
    """)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat messages
chat_container = st.container()
with chat_container:
    for i, msg in enumerate(st.session_state.messages):
        message(msg["content"], is_user=msg["is_user"], key=f"msg_{i}")

# Chat input
if prompt := st.chat_input("Ask about LEGO set prices..."):
    # Add user message to chat
    st.session_state.messages.append({"content": prompt, "is_user": True})
    
    # Display user message immediately
    with chat_container:
        message(prompt, is_user=True, key=f"user_{len(st.session_state.messages)}")
    
    # Show loading spinner
    with st.spinner("🤔 Looking up LEGO set information..."):
        try:
            # Send to FastAPI backend
            backend_url = "http://backend:8000/chat"
            response = requests.post(
                backend_url, 
                json={"query": prompt},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("response", "No response received")
                context = data.get("context", "")
                set_info = data.get("set_info", {})
                
                # Format the response nicely
                formatted_response = bot_response
                
                # Add set info if available
                if set_info:
                    formatted_response += f"\n\n📋 **Set Details:**"
                    formatted_response += f"\n• Name: {set_info.get('name', 'N/A')}"
                    formatted_response += f"\n• Set Number: {set_info.get('set_num', 'N/A')}"
                    formatted_response += f"\n• Pieces: {set_info.get('pieces', 'N/A')}"
                    formatted_response += f"\n• Year: {set_info.get('year', 'N/A')}"
                
                # Add context if available and different from set_info
                if context and not set_info:
                    formatted_response += f"\n\n🔍 *Context: {context}*"
                
                st.session_state.messages.append({
                    "content": formatted_response, 
                    "is_user": False
                })
                
                # Display bot response
                with chat_container:
                    message(formatted_response, key=f"bot_{len(st.session_state.messages)}")
                    
            else:
                error_msg = f"❌ Error: Could not get response (Status: {response.status_code})"
                if response.status_code == 404:
                    error_msg = "❌ Backend service not found. Please check if the backend is running."
                elif response.status_code == 500:
                    error_msg = "❌ Server error. Please try again or check the backend logs."
                
                st.session_state.messages.append({
                    "content": error_msg, 
                    "is_user": False
                })
                
                with chat_container:
                    message(error_msg, key=f"error_{len(st.session_state.messages)}")
                    
        except requests.exceptions.ConnectionError:
            error_msg = "❌ Cannot connect to backend. Please ensure the backend service is running."
            st.session_state.messages.append({
                "content": error_msg, 
                "is_user": False
            })
            with chat_container:
                message(error_msg, key=f"conn_error_{len(st.session_state.messages)}")
                
        except requests.exceptions.Timeout:
            error_msg = "⏱️ Request timed out. The backend might be processing your request."
            st.session_state.messages.append({
                "content": error_msg, 
                "is_user": False
            })
            with chat_container:
                message(error_msg, key=f"timeout_{len(st.session_state.messages)}")
                
        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            st.session_state.messages.append({
                "content": error_msg, 
                "is_user": False
            })
            with chat_container:
                message(error_msg, key=f"unexpected_{len(st.session_state.messages)}")

# Footer
st.markdown("---")
st.markdown("*Powered by Rebrickable API and AI • Prices are estimates and may vary*")