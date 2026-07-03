import docker
from jarvis_core.core.types import Action, PermissionLevel

def containers():
    client = docker.from_env()
    return [
        {"name": c.name, "status": c.status, "image": c.image.tags[0] if c.image.tags else "unknown"}
        for c in client.containers.list(all=True)
    ]

def restart_container(name: str):
    client = docker.from_env()
    c = client.containers.get(name)
    c.restart()
    return {"restarted": name}

ACTIONS = [
    Action("docker.containers", "List Docker containers, their image, and running status.", PermissionLevel.READ, containers, {}),
    Action("docker.restart", "Restart a Docker container by name. Requires confirmation.", PermissionLevel.SAFE_WRITE, restart_container, {"name": "container name"}),
]
