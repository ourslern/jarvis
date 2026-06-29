import json

from app.ollama import chat
from app.tools.system import status
from app.tools.docker_tool import containers
from app.tools.websearch import search
from app.tools.filesystem import list_files, read_file, write_file
from app.memory import remember, recall


def summarize_tool_result(user_message: str, tool_name: str, result, model: str | None = None) -> dict:
    context = (
        "You are Jarvis, Nate's local AI assistant. "
        "A local tool was run successfully. "
        "Summarize the tool result in plain English. "
        "Be concise, practical, and mention anything that needs attention.\n\n"
        f"User request: {user_message}\n"
        f"Tool used: {tool_name}\n"
        f"Tool result JSON:\n{json.dumps(result, indent=2)}"
    )

    response = chat(
        "Summarize this tool result for Nate.",
        model=model,
        context=context,
    )

    return {
        "type": "tool_summary",
        "tool": tool_name,
        "response": response,
        "raw": result,
    }


def route(message: str, model: str | None = None) -> dict:
    m = message.lower().strip()

    if "system status" in m or "how is the ai server" in m or "server status" in m:
        result = status()
        return summarize_tool_result(message, "system.status", result, model)

    if "docker" in m and ("status" in m or "containers" in m or "running" in m):
        result = containers()
        return summarize_tool_result(message, "docker.containers", result, model)

    if m.startswith("search "):
        q = message[7:].strip()
        result = search(q)
        return summarize_tool_result(message, "web.search", result, model)

    if "list files" in m:
        result = list_files()
        return summarize_tool_result(message, "filesystem.list", result, model)

    if m.startswith("read file "):
        result = read_file(message[10:].strip())
        return summarize_tool_result(message, "filesystem.read", result, model)

    if m.startswith("write file "):
        body = message[11:].strip()
        if ":" not in body:
            return {"type": "error", "error": "Use: write file path.txt: content"}
        path, content = body.split(":", 1)
        result = write_file(path.strip(), content.strip())
        return summarize_tool_result(message, "filesystem.write", result, model)

    if m.startswith("remember "):
        body = message[9:].strip()
        if ":" in body:
            k, v = body.split(":", 1)
            result = remember(k.strip(), v.strip())
            return summarize_tool_result(message, "memory.remember", result, model)

    if m.startswith("recall"):
        parts = message.split(maxsplit=1)
        key = parts[1] if len(parts) > 1 else None
        result = recall(key)
        return summarize_tool_result(message, "memory.recall", result, model)

    context = f"Known memory: {recall()}"
    return {"type": "llm", "response": chat(message, model=model, context=context)}
