from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from jarvis_core.skills.loader import build_registry
from jarvis_core.core.agent import JarvisAgent
from jarvis_core.config.settings import WORKSPACE
from fastapi.middleware.cors import CORSMiddleware
from jarvis_core.jobs.global_manager import jobs
from jarvis_core.events.ws_manager import ws_manager

app = FastAPI(title="Jarvis 3 Milestone 2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.1.29:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

registry = build_registry()
agent = JarvisAgent(registry)
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

@app.get("/dashboard/models")
def dashboard_models():
    return {
        "models": registry.run("ollama.models"),
        "running": registry.run("ollama.running"),
    }

@app.post("/api/jobs/ollama/pull/{model_name}")
def job_ollama_pull(model_name: str):
    job = jobs.submit(
        f"Pull Ollama model: {model_name}",
        registry.run,
        "ollama.pull",
        name=model_name,
    )

    return job.to_dict()

import asyncio
from fastapi import WebSocket

@app.get("/api/jobs")
def list_jobs():
    return jobs.all()


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs.get_dict(job_id)
    if not job:
        return {"error": "job not found"}
    return job


@app.post("/api/jobs/{job_id}/cancel")
def cancel_job(job_id: str):
    job = jobs.cancel(job_id)
    if not job:
        return {"error": "job not found"}
    return job.to_dict()

@app.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            system = registry.run("system.status")
            docker = registry.run("docker.containers")
            running = registry.run("ollama.running")
            jarvis = registry.run("jarvis.status")

            gpu = system.get("gpu", {})

            await websocket.send_json({
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
            })

            await asyncio.sleep(3)

    except Exception:
        await websocket.close()

@app.post("/api/docker/{action}/{name}")
def docker_direct_action(action: str, name: str):
    if action == "restart":
        return registry.run("docker.restart", name=name)
    if action == "start":
        return registry.run("docker.start", name=name)
    if action == "stop":
        return registry.run("docker.stop", name=name)
    raise ValueError(f"Unsupported docker action: {action}")

@app.get("/api/docker/logs/{container_name}")
def docker_direct_logs(container_name: str, lines: int = 80):
    return {
        "name": container_name,
        "logs": registry.run("docker.logs", name=container_name, lines=lines),
    }

@app.post("/api/ollama/{action}/{model_name}")
def ollama_direct_action(action: str, model_name: str):
    if action == "load":
        return registry.run("ollama.load", name=model_name)
    if action == "unload":
        return registry.run("ollama.unload", name=model_name)
    if action == "delete":
        return registry.run("ollama.delete", name=model_name)
    if action == "pull":
        return registry.run("ollama.pull", name=model_name)
    raise ValueError(f"Unsupported Ollama action: {action}")

@app.get("/api/ollama/overview")
def ollama_overview():
    return registry.run("ollama.overview")
from fastapi import WebSocket

@app.websocket("/ws/jobs")
async def jobs_socket(ws: WebSocket):

    await ws_manager.connect(ws)

    try:
        while True:
            await ws.receive_text()
    except Exception:
        ws_manager.disconnect(ws)
