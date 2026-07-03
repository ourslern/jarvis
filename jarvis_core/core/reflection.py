import json
from jarvis_core.core.ollama import chat

def summarize(user_message: str, execution: dict, model: str | None = None) -> dict:
    system = "You are Jarvis, Nate's local AI assistant. Summarize action results clearly and mention anything needing attention."
    prompt = f"""
User request:
{user_message}

Execution JSON:
{json.dumps(execution, indent=2)}

Write a concise useful response for Nate.
"""
    response = chat(prompt, model=model, system=system)
    return {"type": "jarvis3_response", "response": response, "raw": execution}
