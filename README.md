# 🧠 LLM Chatbot with FastAPI + Streamlit + Groq API

A lightweight, full-stack AI chatbot built using **FastAPI** as a backend, **Streamlit** for the frontend UI, and integrated with **Groq’s blazing-fast inference API** serving Meta's LLaMA 3 model.

---

## 🚀 Live Demo

- **Frontend UI (Streamlit)** 👉 [Try it live](https://fastapi-app-groq-chatbot-cgqwslw2kbyed4bfdhr2tm.streamlit.app/)
- **Backend API (FastAPI)** 👉 [Open API base](https://fastapi-streamlit-groq-chatbot.onrender.com/)

---

## 🛠 Tech Stack

| Layer       | Tech         |
|-------------|--------------|
| UI          | Streamlit    |
| Backend API | FastAPI      |
| AI Model    | LLaMA 3 (via Groq API) |
| Hosting     | Streamlit Cloud (frontend) & Render (backend) |
| Language    | Python 3.10+ |
| Dependency  | `openai`, `requests`, `pydantic`, `fastapi`, `python-dotenv`, `uvicorn` |

---

## 📦 Project Structure

```bash
FastAPI_Chatbot/
├── .env                      # API Keys and model config (not tracked in Git)
├── main.py                   # FastAPI backend: Receives chat, calls Groq API
├── streamlit_app.py          # Frontend UI: Sends requests to FastAPI endpoint
├── requirements.txt          # All dependencies
└── README.md                 # You're reading it!
```


## 🧠 How It Works
- `main.py`: FastAPI server receives user questions, attaches minimal history, and forwards it to the Groq API.
- `streamlit_app.py`: Streamlit UI handles user interaction and displays responses from the FastAPI backend.
- Uses session memory and concise formatting to keep UX clean and fast.

## ✨ Features
- ⚡ Super fast responses (thanks to Groq's low-latency inference).
- 🧠 Context-aware replies with minimal memory to avoid bloated prompts.
- 🗃️ Downloadable chat transcripts.
- ✅ Clearly separated backend/frontend for easy scaling.
- ☁️ Cloud deployment on Streamlit Cloud and Render for zero-cost hosting.

## 📤 Deployment 
- FastAPI Backend → [Render.com](https://render.com/docs/deploy-fastapi/)
- Streamlit Frontend → [Streamlit Cloud](https://streamlit.io/cloud)

## 🙌 Credits
- [Meta](https://ai.meta.com/llama/) for LLaMA 3
- [Groq](https://groq.com/) for free blazing-fast API access
- [Streamlit](https://streamlit.io/) & [FastAPI](https://fastapi.tiangolo.com/)

## 🧑‍💻 Author
- Deepak Siriboyina – [LinkedIn](https://www.linkedin.com/in/deepak-siriboyina/)
