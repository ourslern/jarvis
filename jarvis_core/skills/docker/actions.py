import docker
from jarvis_core.core.types import Action, PermissionLevel

def containers():
    client = docker.from_env()
    return [
        {"name": c.name, "status": c.status, "image": c.image.tags[0] if c.image.tags else "unknown"}
        for c in client.containers.list(all=True)
    ]



def start_container(name: str):
    client = docker.from_env()
    c = client.containers.get(name)
    c.start()
    return {"started": name}

def stop_container(name: str):
    client = docker.from_env()
    c = client.containers.get(name)
    c.stop()
    return {"stopped": name}

def container_logs(name: str, lines: int = 80, tail: int | None = None):
    client = docker.from_env()
    c = client.containers.get(name)
    count = tail if tail is not None else lines
    raw = c.logs(tail=count, stdout=True, stderr=True, stream=False, timestamps=True)
    return raw.decode("utf-8", errors="replace")

def restart_container(name: str):
    client = docker.from_env()
    c = client.containers.get(name)
    c.restart()
    return {"restarted": name}

ACTIONS = [
    Action("docker.containers", "List Docker containers, their image, and running status.", PermissionLevel.READ, containers, {}),
    Action("docker.restart", "Restart a Docker container by name. Requires confirmation.", PermissionLevel.SAFE_WRITE, restart_container, {"name": "container name"}),

    Action("docker.start", "Start a Docker container by name. Requires confirmation.", PermissionLevel.SAFE_WRITE, start_container, {"name": "container name"}),
    Action("docker.stop", "Stop a Docker container by name. Requires confirmation.", PermissionLevel.SAFE_WRITE, stop_container, {"name": "container name"}),
    Action("docker.logs", "Read recent logs from a Docker container.", PermissionLevel.READ, container_logs, {"name": "container name", "lines": "number of log lines"}),

]
