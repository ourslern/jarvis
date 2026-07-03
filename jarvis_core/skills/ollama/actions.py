from jarvis_core.core.types import Action, PermissionLevel
from jarvis_core.services.ollama_service import OllamaService

ollama = OllamaService()

ACTIONS = [
    Action(
        "ollama.models",
        "List installed Ollama models.",
        PermissionLevel.READ,
        ollama.list_models,
        {},
    ),
    Action(
        "ollama.running",
        "Show currently running Ollama models.",
        PermissionLevel.READ,
        ollama.running_models,
        {},
    ),
    Action(
        "ollama.overview",
        "Show installed and running Ollama models together.",
        PermissionLevel.READ,
        ollama.overview,
        {},
    ),
    Action(
        "ollama.pull",
        "Download or update an Ollama model by name.",
        PermissionLevel.SAFE_WRITE,
        ollama.pull_model,
        {"name": "model name"},
    ),
    Action(
        "ollama.load",
        "Load an Ollama model into memory.",
        PermissionLevel.SAFE_WRITE,
        ollama.load_model,
        {"name": "model name"},
    ),
    Action(
        "ollama.unload",
        "Unload an Ollama model from memory.",
        PermissionLevel.SAFE_WRITE,
        ollama.unload_model,
        {"name": "model name"},
    ),
    Action(
        "ollama.delete",
        "Delete an Ollama model.",
        PermissionLevel.DANGEROUS,
        ollama.delete_model,
        {"name": "model name"},
    ),
]
