# =============================================
# Streamlit Frontend for Groq-Powered LLM Chat
# Integrates with FastAPI backend hosted on Render
# =============================================

import streamlit as st
import requests
from datetime import datetime

# -------------------------------
# Basic Streamlit Configuration
# -------------------------------
st.set_page_config(page_title="LLM Chat", page_icon="🤖")
st.title("🤖 Talk to an LLM powered by Meta's LLaMA3 via FastAPI & Groq")

# ----------------------------------------
# Initialize session state for chat history
# This ensures chat continuity across Streamlit reruns
# ----------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# Input box for user prompt and Submit button
# Wrapped inside a form to control clearing behavior
# --------------------------------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("🧑‍💻 You:", placeholder="Ask me anything...", key="user_input")
    submitted = st.form_submit_button("Send")

# -----------------------------------------------------
# API Call to FastAPI endpoint (Replace with your URL)
# Sends the latest user message and chat history context
# -----------------------------------------------------
if submitted and user_input:
    try:
        api_url = "https://fastapi-streamlit-groq-chatbot.onrender.com/chat/" 

        response = requests.post(
            api_url,
            json={
                "message": user_input,
                "history": st.session_state.chat_history
            }
        )
        if response.status_code == 200:
            bot_reply = response.json()["response"]
        else:
            bot_reply = f"❌ Error: {response.status_code} - {response.text}"
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    # Add latest Q&A to the top of the chat history
    st.session_state.chat_history.insert(0, (user_input, bot_reply))

# -------------------------------------------------------
# Display chat history using collapsible markdown blocks
# Keeps interface clean while preserving full responses
# -------------------------------------------------------
for question, answer in st.session_state.chat_history:
    with st.container():
        st.markdown(f"🧑‍💻 **You:** {question}")
        with st.expander("🤖 **Bot's reply**"):
            st.markdown(answer, unsafe_allow_html=True)
        st.markdown("---")

# -----------------------------------------------------------
# Export Chat: Generate downloadable .txt file of the session
# Useful for saving chat logs locally
# -----------------------------------------------------------
if st.session_state.chat_history:
    def format_chat(chat_list):
        return "\n\n".join([f"You: {q}\nBot: {a}" for q, a in reversed(chat_list)])

    chat_text = format_chat(st.session_state.chat_history)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_{timestamp}.txt"
    
    st.download_button(
        label="💾 Save Conversation",
        data=chat_text,
        file_name=filename,
        mime="text/plain"
    )
