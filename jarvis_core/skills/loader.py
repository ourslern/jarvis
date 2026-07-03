from jarvis_core.core.registry import ActionRegistry
from jarvis_core.skills.system.actions import ACTIONS as SYSTEM_ACTIONS
from jarvis_core.skills.docker.actions import ACTIONS as DOCKER_ACTIONS
from jarvis_core.skills.websearch.actions import ACTIONS as WEB_ACTIONS
from jarvis_core.skills.filesystem.actions import ACTIONS as FILE_ACTIONS

def build_registry() -> ActionRegistry:
    registry = ActionRegistry()
    for action in [*SYSTEM_ACTIONS, *DOCKER_ACTIONS, *WEB_ACTIONS, *FILE_ACTIONS]:
        registry.register(action)
    return registry
