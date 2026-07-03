import importlib
import pkgutil
from jarvis_core.skills import __path__ as skills_path

def discover_skill_actions():
    actions = []

    for module_info in pkgutil.iter_modules(skills_path):
        name = module_info.name

        if name.startswith("_") or name in {"loader"}:
            continue

        try:
            module = importlib.import_module(f"jarvis_core.skills.{name}.actions")
            skill_actions = getattr(module, "ACTIONS", [])
            actions.extend(skill_actions)
        except ModuleNotFoundError:
            continue

    return actions
