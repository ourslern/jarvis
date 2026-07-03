import os
import time
import psutil
from jarvis_core.core.types import Action, PermissionLevel

START_TIME = time.time()

def jarvis_status():
    process = psutil.Process(os.getpid())
    uptime_seconds = round(time.time() - START_TIME, 1)

    return {
        "status": "running",
        "pid": os.getpid(),
        "uptime_seconds": uptime_seconds,
        "uptime_minutes": round(uptime_seconds / 60, 2),
        "memory_mb": round(process.memory_info().rss / 1024**2, 2),
        "cpu_percent": process.cpu_percent(interval=0.2),
    }

ACTIONS = [
    Action(
        name="jarvis.status",
        description="Show Jarvis service health, uptime, PID, memory usage, and CPU usage.",
        permission=PermissionLevel.READ,
        function=jarvis_status,
        args_schema={},
    )
]
