from app.ollama import chat
from app.tools.system import status
from app.tools.docker_tool import containers
from app.tools.websearch import search
from app.tools.filesystem import list_files, read_file, write_file
from app.memory import remember, recall

def route(message: str, model: str | None = None) -> dict:
    m = message.lower().strip()

    if "system status" in m or "how is the ai server" in m or "server status" in m:
        return {"type": "tool", "tool": "system.status", "result": status()}

    if "docker" in m and ("status" in m or "containers" in m or "running" in m):
        return {"type": "tool", "tool": "docker.containers", "result": containers()}

    if m.startswith("search "):
        q = message[7:].strip()
        return {"type": "tool", "tool": "web.search", "result": search(q)}

    if "list files" in m:
        return {"type": "tool", "tool": "filesystem.list", "result": list_files()}

    if m.startswith("read file "):
        return {"type": "tool", "tool": "filesystem.read", "result": read_file(message[10:].strip())}

    if m.startswith("write file "):
        # Format: write file path.txt: content here
        body = message[11:].strip()
        if ":" not in body:
            return {"type": "error", "error": "Use: write file path.txt: content"}
        path, content = body.split(":", 1)
        return {"type": "tool", "tool": "filesystem.write", "result": write_file(path.strip(), content.strip())}

    if m.startswith("remember "):
        body = message[9:].strip()
        if ":" in body:
            k, v = body.split(":", 1)
            return {"type": "tool", "tool": "memory.remember", "result": remember(k.strip(), v.strip())}

    if m.startswith("recall"):
        parts = message.split(maxsplit=1)
        key = parts[1] if len(parts) > 1 else None
        return {"type": "tool", "tool": "memory.recall", "result": recall(key)}

    context = f"Known memory: {recall()}"
    return {"type": "llm", "response": chat(message, model=model, context=context)}
