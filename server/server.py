import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

load_dotenv()

# server için key
API_KEY = os.getenv("API_KEY")
# vllm kısmı
VLLM_HOST = os.getenv("VLLM_HOST", "localhost")
VLLM_PORT = os.getenv("VLLM_PORT", "8080")
MODEL_NAME = os.getenv("MODEL_NAME")
# url .env içerisinden dinamik okunuuyo
VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", f"http://{VLLM_HOST}:{VLLM_PORT}/v1")


app = FastAPI(title="LLM Demo Server")

class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def root():
    return {
        "status": "ok",
        "model": MODEL_NAME,
    }


@app.get("/models")
async def models(x_api_key: str | None = Header(default=None)):
    check_api_key(x_api_key)

    return {
        "model": MODEL_NAME,
    }


@app.post("/chat")
async def chat(
    request: ChatRequest,
    x_api_key: str | None = Header(default=None),
):
    check_api_key(x_api_key)

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": request.message,
            }
        ],
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{VLLM_BASE_URL}/chat/completions",
            json=payload,
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    data = response.json()

    return {
        "message": data["choices"][0]["message"]["content"],
        "usage": data.get("usage"),
        "model": MODEL_NAME,
    }


def check_api_key(api_key: str | None):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )