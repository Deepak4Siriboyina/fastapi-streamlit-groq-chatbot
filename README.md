# fastapi-streamlit-groq-chatbot
LLM chatbot using FastAPI backend, Streamlit frontend, and Groq API integration.

# 🧠 LLM Chatbot with FastAPI + Streamlit + Groq API

This project is a lightweight LLM chatbot that combines a **FastAPI backend**, a **Streamlit frontend**, and uses **Groq’s blazing-fast LLaMA 3 API** for inference.

![architecture](Image_link)

---

## 🚀 Tech Stack

- **FastAPI** – Backend API handling LLM interaction logic.
- **Streamlit** – Simple, elegant UI for chatting with the LLM.
- **Groq API** – Lightning-fast inference with LLaMA 3 (8B) model.
- **OpenAI SDK** – For Groq-compatible interaction.
- **Python 3.10+**

---

## 📁 Project Structure

FastAPI_Chatbot/
│
├── main.py # FastAPI backend with Groq API
├── streamlit_app.py # Streamlit frontend UI
├── requirements.txt # All Python dependencies
├── .gitignore # Ignore virtualenv and .env
├── .env # Contains GROQ_API_KEY and model (Not committed)
└── README.md # Project overview (this file)

