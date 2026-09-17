import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from power import GpuPowerMonitor

load_dotenv()

# server için key
API_KEY = os.getenv("API_KEY")
# llm backend
LLM_HOST = os.getenv("LLM_HOST", "localhost")
LLM_PORT = os.getenv("LLM_PORT", "11434")
MODEL_NAME = os.getenv("MODEL_NAME")
# url .env içerisinden dinamik okunuuyo
LLM_BASE_URL = os.getenv("LLM_BASE_URL", f"http://{LLM_HOST}:{LLM_PORT}/v1")
ELECTRICITY_PRICE_TL_PER_KWH = float(os.getenv("ELECTRICITY_PRICE_TL_PER_KWH", "0"))


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

    monitor = GpuPowerMonitor()
    monitor.start()

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            json=payload,
        )

    energy = monitor.stop()
    energy["cost_tl"] = round(
        (energy["energy_wh"] / 1000) * ELECTRICITY_PRICE_TL_PER_KWH, 6
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
        "energy": energy,
    }


def check_api_key(api_key: str | None):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )