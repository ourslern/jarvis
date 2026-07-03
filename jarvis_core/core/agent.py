from jarvis_core.core.decision_engine import choose_actions
from jarvis_core.core.executor import execute_plan
from jarvis_core.core.reflection import summarize
from jarvis_core.core.ollama import chat
from jarvis_core.memory.store import recall, remember

class JarvisAgent:
    def __init__(self, registry):
        self.registry = registry

    def handle(self, message: str, model: str | None = None, confirmed: bool = False) -> dict:
        lower = message.lower().strip()

        if lower.startswith("remember "):
            body = message[9:].strip()
            if ":" in body:
                key, value = body.split(":", 1)
                return {"type": "memory", "result": remember(key.strip(), value.strip())}

        if lower.startswith("recall"):
            parts = message.split(maxsplit=1)
            key = parts[1] if len(parts) > 1 else None
            return {"type": "memory", "result": recall(key)}

        decision = choose_actions(message, self.registry.list_actions(), model=model)
        if decision.get("steps"):
            execution = execute_plan(decision, self.registry, confirmed=confirmed)
            return summarize(message, execution, model=model)

        return {"type": "llm", "response": chat(message, model=model, system=f"Known memory: {recall()}")}
