from pathlib import Path
from jarvis_core.config.settings import WORKSPACE
from jarvis_core.core.types import Action, PermissionLevel

WORKSPACE.mkdir(parents=True, exist_ok=True)

def safe_path(path: str) -> Path:
    p = (WORKSPACE / path).resolve()
    if not str(p).startswith(str(WORKSPACE.resolve())):
        raise ValueError("Path outside workspace is not allowed")
    return p

def list_files():
    return [str(p.relative_to(WORKSPACE)) for p in WORKSPACE.rglob("*")]

def read_file(path: str):
    return safe_path(path).read_text()

def write_file(path: str, content: str):
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return {"written": str(p)}

ACTIONS = [
    Action("filesystem.list", "List files in Jarvis workspace.", PermissionLevel.READ, list_files, {}),
    Action("filesystem.read", "Read a file from Jarvis workspace.", PermissionLevel.READ, read_file, {"path": "relative workspace file path"}),
    Action("filesystem.write", "Write a file inside Jarvis workspace. Requires confirmation.", PermissionLevel.SAFE_WRITE, write_file, {"path": "relative workspace file path", "content": "file content"}),
]
