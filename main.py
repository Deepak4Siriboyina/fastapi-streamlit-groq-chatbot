from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import re
from openai import OpenAI

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY not found in .env file.")

# ✅ Correct Groq-compatible OpenAI client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: list[list[str]] = []

def clean_bot_response(response: str) -> str:
    cleaned = re.split(r'\b(?:Human:|AI:|You:|User:)\b', response)[0].strip()
    cleaned = re.sub(r'[\n\r]+', ' ', cleaned)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
    MAX_CHARS = 300
    return cleaned[:MAX_CHARS] if cleaned else "I'm not sure how to answer that."

@app.get("/")
def root():
    return {"message": "✅ FastAPI backend is running. Use POST /chat/ to interact with the chatbot."}

@app.post("/chat/")
def chat(req: ChatRequest):
    try:
        # Build chat history context
        messages = [{"role": "system", "content": "You are a helpful and concise assistant. Answer in 1-2 short sentences only."}]
        if req.history:
            for q, a in req.history[-3:]:  # Include last 3 Q&A pairs
                messages.append({"role": "user", "content": q})
                messages.append({"role": "assistant", "content": a})
        messages.append({"role": "user", "content": req.message})

        # 🧠 Chat completion with Groq's LLaMA model
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=100,
            stop=["Human:", "AI:"]
        )

        raw_output = response.choices[0].message.content
        cleaned = clean_bot_response(raw_output)
        return {"response": cleaned}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
