import requests
from app.config import OLLAMA_URL, JARVIS_MODEL

def chat(message: str, model: str | None = None, context: str = "") -> str:
    payload = {
        "model": model or JARVIS_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Jarvis, Nate's persistent local AI assistant running on Ubuntu. "
                    "Be practical, concise, and helpful. Use available tool results when provided. "
                    + context
                ),
            },
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=300)
    r.raise_for_status()
    return r.json().get("message", {}).get("content", "")
