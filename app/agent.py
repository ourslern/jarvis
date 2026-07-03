import json

from app.ollama import chat
from app.memory import remember, recall
from app.tool_registry import run_tool
from app.planner import make_plan, run_plan

# Register tools
import app.tools.system
import app.tools.docker_tool
import app.tools.websearch
import app.tools.filesystem


def summarize(user_message: str, tool_data, model: str | None = None) -> dict:
    context = (
        "You are Jarvis, Nate's local AI assistant. "
        "You ran local tools successfully. Summarize the results in plain English. "
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

    plan = make_plan(message)
    if plan:
        results = run_plan(plan)
        return summarize(message, {"plan": plan, "results": results}, model)

    if "docker" in m and ("status" in m or "containers" in m or "running" in m):
        result = run_tool("docker.containers")
        return summarize(message, [{"tool": "docker.containers", "result": result}], model)

    if m.startswith("search "):
        q = message[7:].strip()
        result = run_tool("web.search", query=q)
        return summarize(message, [{"tool": "web.search", "result": result}], model)

    if "list files" in m:
        result = run_tool("filesystem.list")
        return summarize(message, [{"tool": "filesystem.list", "result": result}], model)

    if m.startswith("read file "):
        result = run_tool("filesystem.read", path=message[10:].strip())
        return summarize(message, [{"tool": "filesystem.read", "result": result}], model)

    if m.startswith("write file "):
        body = message[11:].strip()
        if ":" not in body:
            return {"type": "error", "error": "Use: write file path.txt: content"}
        path, content = body.split(":", 1)
        result = run_tool("filesystem.write", path=path.strip(), content=content.strip())
        return summarize(message, [{"tool": "filesystem.write", "result": result}], model)

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

    context = f"Known memory: {recall()}"
    return {"type": "llm", "response": chat(message, model=model, context=context)}
