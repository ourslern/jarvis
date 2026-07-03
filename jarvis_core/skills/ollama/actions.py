import requests
from jarvis_core.config.settings import OLLAMA_URL
from jarvis_core.core.types import Action, PermissionLevel

def list_models():
    r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
    r.raise_for_status()
    data = r.json()
    return [
        {
            "name": m.get("name"),
            "size_gb": round((m.get("size") or 0) / 1024**3, 2),
            "modified_at": m.get("modified_at"),
        }
        for m in data.get("models", [])
    ]

def running_models():
    r = requests.get(f"{OLLAMA_URL}/api/ps", timeout=10)
    r.raise_for_status()
    return r.json().get("models", [])

def pull_model(name: str):
    r = requests.post(
        f"{OLLAMA_URL}/api/pull",
        json={"name": name, "stream": False},
        timeout=1800,
    )
    r.raise_for_status()
    return r.json()

ACTIONS = [
    Action(
        name="ollama.models",
        description="List installed Ollama models.",
        permission=PermissionLevel.READ,
        function=list_models,
        args_schema={},
    ),
    Action(
        name="ollama.running",
        description="Show currently running Ollama models.",
        permission=PermissionLevel.READ,
        function=running_models,
        args_schema={},
    ),
    Action(
        name="ollama.pull",
        description="Download/pull an Ollama model by name. Requires confirmation.",
        permission=PermissionLevel.SAFE_WRITE,
        function=pull_model,
        args_schema={"name": "model name, for example qwen3:14b"},
    ),
]
