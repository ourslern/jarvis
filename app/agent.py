import json

from app.ollama import chat
from app.memory import remember, recall
from app.decision_engine import choose_tools, execute_decision

# Register tools
import app.tools.system
import app.tools.docker_tool
import app.tools.websearch
import app.tools.filesystem


def summarize(user_message: str, tool_data, model: str | None = None) -> dict:
    context = (
        "You are Jarvis, Nate's local AI assistant. "
        "You used local tools. Summarize the results in plain English. "
        "Be concise, practical, and mention anything that needs attention.\n\n"
        f"User request: {user_message}\n"
        f"Tool data JSON:\n{json.dumps(tool_data, indent=2)}"
    )

    response = chat("Summarize these tool results for Nate.", model=model, context=context)

    return {
        "type": "tool_summary",
        "response": response,
        "raw": tool_data,
    }


def route(message: str, model: str | None = None) -> dict:
    m = message.lower().strip()

    if m.startswith("remember "):
        body = message[9:].strip()
        if ":" in body:
            k, v = body.split(":", 1)
            result = remember(k.strip(), v.strip())
            return summarize(message, [{"tool": "memory.remember", "result": result}], model)

    if m.startswith("recall"):
        parts = message.split(maxsplit=1)
        key = parts[1] if len(parts) > 1 else None
        result = recall(key)
        return summarize(message, [{"tool": "memory.recall", "result": result}], model)

    decision = choose_tools(message, model=model)

    if decision.get("steps"):
        execution = execute_decision(decision)
        return summarize(message, execution, model)

    context = f"Known memory: {recall()}"
    return {"type": "llm", "response": chat(message, model=model, context=context)}
