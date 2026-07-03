import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(os.getenv("JARVIS_BASE_DIR", Path.home() / "jarvis"))
load_dotenv(BASE_DIR / "config" / "settings.env")

JARVIS_MODEL = os.getenv("JARVIS_MODEL", "qwen3:8b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://127.0.0.1:8081")
WORKSPACE = Path(os.getenv("WORKSPACE", str(BASE_DIR / "workspace")))
MEMORY_FILE = BASE_DIR / "memory" / "jarvis3_memory.json"
