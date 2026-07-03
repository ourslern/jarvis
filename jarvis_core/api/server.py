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
