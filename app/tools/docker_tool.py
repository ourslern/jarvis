import docker
from app.tool_registry import tool

@tool("docker.containers", "List Docker containers, their image, and running status.", read_only=True)
def containers():
    client = docker.from_env()
    output = []
    for c in client.containers.list(all=True):
        output.append({
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "unknown",
        })
    return output

@tool("docker.restart", "Restart a Docker container by name.", read_only=False)
def restart_container(name: str):
    client = docker.from_env()
    c = client.containers.get(name)
    c.restart()
    return {"restarted": name}
