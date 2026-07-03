import time
from typing import Callable, Any

TOOLS = {}
ACTION_LOG = []

def tool(name: str, description: str, read_only: bool = True):
    def decorator(func: Callable):
        TOOLS[name] = {
            "name": name,
            "description": description,
            "read_only": read_only,
            "function": func,
        }
        return func
    return decorator

def list_tools():
    return [
        {
            "name": t["name"],
            "description": t["description"],
            "read_only": t["read_only"],
        }
        for t in TOOLS.values()
    ]

def run_tool(name: str, **kwargs) -> dict:
    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")

    started = time.time()
    result = TOOLS[name]["function"](**kwargs)

    entry = {
        "timestamp": started,
        "tool": name,
        "args": kwargs,
        "result": result,
        "duration_sec": round(time.time() - started, 3),
    }
    ACTION_LOG.append(entry)

    return result

def get_action_log(limit: int = 25):
    return ACTION_LOG[-limit:]
