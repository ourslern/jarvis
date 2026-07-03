from jarvis_core.core.registry import ActionRegistry
from jarvis_core.skills.discovery import discover_skill_actions

def build_registry() -> ActionRegistry:
    registry = ActionRegistry()

    for action in discover_skill_actions():
        registry.register(action)

    return registry
