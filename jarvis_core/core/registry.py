import time
from jarvis_core.core.types import Action

class ActionRegistry:
    def __init__(self):
        self.actions: dict[str, Action] = {}
        self.action_log: list[dict] = []

    def register(self, action: Action):
        self.actions[action.name] = action

    def list_actions(self) -> list[dict]:
        return [
            {
                "name": a.name,
                "description": a.description,
                "permission": a.permission.value,
                "args_schema": a.args_schema or {},
            }
            for a in self.actions.values()
        ]

    def run(self, name: str, **kwargs):
        if name not in self.actions:
            raise ValueError(f"Unknown action: {name}")
        started = time.time()
        action = self.actions[name]
        result = action.function(**kwargs)
        self.action_log.append({
            "timestamp": started,
            "action": name,
            "args": kwargs,
            "result": result,
            "duration_sec": round(time.time() - started, 3),
        })
        return result

    def logs(self, limit: int = 25):
        return self.action_log[-limit:]
