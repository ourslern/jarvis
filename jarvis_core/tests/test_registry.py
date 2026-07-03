from jarvis_core.skills.loader import build_registry

def test_registry_loads_actions():
    registry = build_registry()
    names = [a["name"] for a in registry.list_actions()]
    assert "system.status" in names
    assert "docker.containers" in names
    assert "web.search" in names
    assert "filesystem.list" in names
