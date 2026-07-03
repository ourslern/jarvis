from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import route
from app.ollama import chat
from app.memory import remember, recall
from app.tools.system import status
from app.tools.docker_tool import containers, restart_container
from app.tools.websearch import search
from app.tools.filesystem import list_files, read_file, write_file
from app.config import WORKSPACE
from app.tool_registry import list_tools, get_action_log

app = FastAPI(title="Jarvis v1")

class ChatRequest(BaseModel):
    message: str
    model: str | None = None

class MemoryRequest(BaseModel):
    key: str
    value: str

class FileWriteRequest(BaseModel):
    path: str
    content: str

@app.get("/")
def root():
    return {"status": "Jarvis v1 online"}

@app.get("/health")
def health():
    return {"status": "ok", "workspace": str(WORKSPACE)}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return route(req.message, model=req.model)

@app.post("/llm")
def llm_endpoint(req: ChatRequest):
    return {"response": chat(req.message, model=req.model)}

@app.get("/status")
def status_endpoint():
    return status()

@app.get("/docker")
def docker_endpoint():
    return {"containers": containers()}

@app.post("/docker/restart/{name}")
def docker_restart_endpoint(name: str):
    return restart_container(name)

@app.get("/search")
def search_endpoint(q: str):
    return {"results": search(q)}

@app.get("/files")
def files_endpoint():
    return {"files": list_files()}

@app.get("/files/read")
def read_file_endpoint(path: str):
    return {"path": path, "content": read_file(path)}

@app.post("/files/write")
def write_file_endpoint(req: FileWriteRequest):
    return write_file(req.path, req.content)

@app.get("/memory")
def memory_get():
    return recall()

@app.post("/memory")
def memory_set(req: MemoryRequest):
    return remember(req.key, req.value)


@app.get("/tools")
def tools_endpoint():
    return {"tools": list_tools()}

@app.get("/actions")
def actions_endpoint(limit: int = 25):
    return {"actions": get_action_log(limit)}
