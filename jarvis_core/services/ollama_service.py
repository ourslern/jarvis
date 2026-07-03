import requests
from jarvis_core.config.settings import OLLAMA_URL


class OllamaService:
    def __init__(self, base_url: str = OLLAMA_URL):
        self.base_url = base_url.rstrip("/")

    def list_models(self):
        r = requests.get(f"{self.base_url}/api/tags", timeout=10)
        r.raise_for_status()
        data = r.json()
        return [
            {
                "name": m.get("name"),
                "size_gb": round((m.get("size") or 0) / 1024**3, 2),
                "modified_at": m.get("modified_at"),
            }
            for m in data.get("models", [])
        ]

    def running_models(self):
        r = requests.get(f"{self.base_url}/api/ps", timeout=10)
        r.raise_for_status()
        return r.json().get("models", [])

    def pull_model(self, name: str):
        r = requests.post(
            f"{self.base_url}/api/pull",
            json={"name": name, "stream": False},
            timeout=1800,
        )
        r.raise_for_status()
        return r.json()

    def load_model(self, name: str):
        r = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": name,
                "prompt": "",
                "keep_alive": "30m",
                "stream": False,
            },
            timeout=300,
        )
        r.raise_for_status()
        return {"loaded": name}

    def unload_model(self, name: str):
        r = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": name,
                "prompt": "",
                "keep_alive": 0,
                "stream": False,
            },
            timeout=60,
        )
        r.raise_for_status()
        return {"unloaded": name}

    def delete_model(self, name: str):
        r = requests.delete(
            f"{self.base_url}/api/delete",
            json={"name": name},
            timeout=60,
        )
        r.raise_for_status()
        return {"deleted": name}

    def overview(self):
        installed = self.list_models()
        running = self.running_models()
        running_names = {m.get("name") for m in running}

        return {
            "models": [
                {
                    **m,
                    "loaded": m["name"] in running_names,
                }
                for m in installed
            ],
            "running": running,
        }
