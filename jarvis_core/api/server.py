from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from jarvis_core.skills.loader import build_registry
from jarvis_core.core.agent import JarvisAgent
from jarvis_core.config.settings import WORKSPACE

registry = build_registry()
agent = JarvisAgent(registry)
app = FastAPI(title="Jarvis 3 Milestone 2")
app.mount("/static", StaticFiles(directory="jarvis_core/api/static"), name="static")

class ChatRequest(BaseModel):
    message: str
    model: str | None = None
    confirmed: bool = False

@app.get("/")
def root():
    return {"status": "Jarvis 3 Milestone 1 online"}

@app.get("/health")
def health():
    return {"status": "ok", "workspace": str(WORKSPACE)}

@app.get("/skills")
def skills():
    return {"actions": registry.list_actions()}

@app.get("/actions")
def actions(limit: int = 25):
    return {"actions": registry.logs(limit)}

@app.post("/chat")
def chat(req: ChatRequest):
    return agent.handle(req.message, model=req.model, confirmed=req.confirmed)


@app.get("/dashboard")
def dashboard():
    return FileResponse("jarvis_core/api/static/index.html")

@app.get("/dashboard/status")
def dashboard_status():
    return {
        "system": registry.run("system.status"),
        "docker": registry.run("docker.containers"),
        "ollama_running": registry.run("ollama.running"),
    }

@app.get("/dashboard/models")
def dashboard_models():
    return {
        "models": registry.run("ollama.models"),
        "running": registry.run("ollama.running"),
    }

@app.get("/dashboard/jarvis")
def dashboard_jarvis():
    return {
        "jarvis": registry.run("jarvis.status"),
        "recent_actions": registry.logs(10),
    }

@app.get("/dashboard/live")
def dashboard_live():
    system = registry.run("system.status")
    docker = registry.run("docker.containers")
    running = registry.run("ollama.running")
    jarvis = registry.run("jarvis.status")

    gpu = system.get("gpu", {})

    return {
        "system": {
            "cpu_percent": system.get("cpu_percent"),
            "ram_percent": system.get("ram_percent"),
            "disk_percent": system.get("disk_percent"),
        },
        "gpu": {
            "name": gpu.get("name"),
            "util_percent": gpu.get("util_percent"),
            "memory_used_mb": gpu.get("memory_used_mb"),
            "memory_total_mb": gpu.get("memory_total_mb"),
            "temperature_c": gpu.get("temperature_c"),
            "power_watts": gpu.get("power_watts"),
        },
        "docker": {
            "running": len([c for c in docker if c.get("status") == "running"]),
            "total": len(docker),
            "containers": docker,
        },
        "ollama": {
            "running_models": running,
        },
        "jarvis": jarvis,
    }
