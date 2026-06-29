from pathlib import Path
from app.config import WORKSPACE

WORKSPACE.mkdir(parents=True, exist_ok=True)

def safe_path(path: str) -> Path:
    p = (WORKSPACE / path).resolve()
    if not str(p).startswith(str(WORKSPACE.resolve())):
        raise ValueError("Path outside workspace is not allowed")
    return p

def list_files() -> list[str]:
    return [str(p.relative_to(WORKSPACE)) for p in WORKSPACE.rglob("*")]

def read_file(path: str) -> str:
    return safe_path(path).read_text()

def write_file(path: str, content: str) -> dict:
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return {"written": str(p)}
