import docker

def containers() -> list[dict]:
    client = docker.from_env()
    output = []
    for c in client.containers.list(all=True):
        output.append({
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "unknown",
        })
    return output

def restart_container(name: str) -> dict:
    client = docker.from_env()
    c = client.containers.get(name)
    c.restart()
    return {"restarted": name}
