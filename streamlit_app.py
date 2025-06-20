import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="LLM Chat", page_icon="🤖")

# Title
st.title("🤖 Talk to an LLM powered by Meta's LLaMA3 via FastAPI & Groq")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field and submission
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("🧑‍💻 You:", placeholder="Ask me anything...", key="user_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    try:
        # ⛳ Replace with your actual Render backend URL
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

    # Add latest Q&A to the top of chat history
    st.session_state.chat_history.insert(0, (user_input, bot_reply))

# Display collapsible Q&A with avatars and markdown
for question, answer in st.session_state.chat_history:
    with st.container():
        st.markdown(f"🧑‍💻 **You:** {question}")
        with st.expander("🤖 **Bot's reply**"):
            st.markdown(answer, unsafe_allow_html=True)
        st.markdown("---")

# Save chat button
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
