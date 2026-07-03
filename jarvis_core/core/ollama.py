import requests
from jarvis_core.config.settings import OLLAMA_URL, JARVIS_MODEL

def chat(message: str, model: str | None = None, system: str | None = None, timeout: int = 300) -> str:
    payload = {
        "model": model or JARVIS_MODEL,
        "messages": [
            {"role": "system", "content": system or "You are Jarvis, Nate's local AI assistant. Be concise and practical."},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json().get("message", {}).get("content", "")
