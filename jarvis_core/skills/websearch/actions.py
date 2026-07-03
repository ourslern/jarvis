import requests
from jarvis_core.config.settings import SEARXNG_URL
from jarvis_core.core.types import Action, PermissionLevel

def search(query: str, limit: int = 5):
    r = requests.get(f"{SEARXNG_URL}/search", params={"q": query, "format": "json"}, timeout=20)
    r.raise_for_status()
    data = r.json()
    return [
        {"title": x.get("title"), "url": x.get("url"), "content": x.get("content"), "engine": x.get("engine")}
        for x in data.get("results", [])[:limit]
    ]

ACTIONS = [
    Action("web.search", "Search the web using local SearXNG.", PermissionLevel.READ, search, {"query": "search query", "limit": "optional result count"})
]
