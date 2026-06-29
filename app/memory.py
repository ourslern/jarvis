import json
from app.config import MEMORY_FILE

def _load() -> dict:
    if not MEMORY_FILE.exists():
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        MEMORY_FILE.write_text("{}")
    return json.loads(MEMORY_FILE.read_text())

def remember(key: str, value: str) -> dict:
    data = _load()
    data[key] = value
    MEMORY_FILE.write_text(json.dumps(data, indent=2))
    return {"saved": True, "key": key, "value": value}

def recall(key: str | None = None) -> dict:
    data = _load()
    if key:
        return {key: data.get(key)}
    return data
