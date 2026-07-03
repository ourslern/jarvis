import requests
from app.config import SEARXNG_URL
from app.tool_registry import tool

@tool("web.search", "Search the web using local SearXNG.", read_only=True)
def search(query: str, limit: int = 5):
    r = requests.get(
        f"{SEARXNG_URL}/search",
        params={"q": query, "format": "json"},
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()
    results = data.get("results", [])[:limit]
    return [
        {
            "title": x.get("title"),
            "url": x.get("url"),
            "content": x.get("content"),
            "engine": x.get("engine"),
        }
        for x in results
    ]
