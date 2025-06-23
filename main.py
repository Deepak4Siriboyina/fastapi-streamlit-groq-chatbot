# ============================================
# FastAPI Backend for Groq-Powered Chatbot
# ============================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import re
from openai import OpenAI

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY not found in .env file.")

# -----------------------------------------------------
# Initialize Groq-compatible OpenAI API client
# -----------------------------------------------------
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"  # Note: Groq uses OpenAI-compatible schema
)

# ----------------------------------
# FastAPI app initialization
# ----------------------------------
app = FastAPI()

# ------------------------------------------
# Define the request schema using Pydantic
# ------------------------------------------
class ChatRequest(BaseModel):
    message: str                      # User's latest input
    history: list[list[str]] = []     # Optional prior Q&A context

# ------------------------------------------------------------
# Utility: Clean model response to avoid hallucinated dialogue
# ------------------------------------------------------------
def clean_bot_response(response: str) -> str:
    # Remove trailing AI-generated "Human:" or "AI:" continuations
    cleaned = re.split(r'\b(?:Human:|AI:|You:|User:)\b', response)[0].strip()
    # Normalize spacing and line breaks
    cleaned = re.sub(r'[\n\r]+', ' ', cleaned)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
    # Limit length to avoid runaway text
    MAX_CHARS = 300
    return cleaned[:MAX_CHARS] if cleaned else "I'm not sure how to answer that."

# ---------------------------------------------------------
# Root route - useful for checking Render deployment
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "✅ FastAPI backend is running. Use POST /chat/ to interact with the chatbot."}

# ---------------------------------------------------------
# Chat endpoint - handles LLM completion with context
# ---------------------------------------------------------
@app.post("/chat/")
def chat(req: ChatRequest):
    try:
        # → Create structured message history for LLM
        messages = [{"role": "system", "content": "You are a helpful and concise assistant. Answer in 1-2 short sentences only."}]
        
        if req.history:
            # Append last 3 user-bot interactions to maintain minimal context
            for q, a in req.history[-3:]:
                messages.append({"role": "user", "content": q})
                messages.append({"role": "assistant", "content": a})
        
        # Add the new user query to the end of the message list
        messages.append({"role": "user", "content": req.message})

        # → Call Groq API with formatted prompt
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=100,
            stop=["Human:", "AI:"]
        )

        # Extract and clean model response before sending it to frontend
        raw_output = response.choices[0].message.content
        cleaned = clean_bot_response(raw_output)
        return {"response": cleaned}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
