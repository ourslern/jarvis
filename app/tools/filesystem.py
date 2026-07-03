from pathlib import Path
from app.config import WORKSPACE
from app.tool_registry import tool

WORKSPACE.mkdir(parents=True, exist_ok=True)

def safe_path(path: str) -> Path:
    p = (WORKSPACE / path).resolve()
    if not str(p).startswith(str(WORKSPACE.resolve())):
        raise ValueError("Path outside workspace is not allowed")
    return p

@tool("filesystem.list", "List files in Jarvis workspace.", read_only=True)
def list_files():
    return [str(p.relative_to(WORKSPACE)) for p in WORKSPACE.rglob("*")]

@tool("filesystem.read", "Read a file from Jarvis workspace.", read_only=True)
def read_file(path: str):
    return safe_path(path).read_text()

@tool("filesystem.write", "Write a file inside Jarvis workspace.", read_only=False)
def write_file(path: str, content: str):
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return {"written": str(p)}
