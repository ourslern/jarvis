from dataclasses import dataclass, field
from time import time
from uuid import uuid4
from typing import Any


@dataclass
class Job:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    status: str = "queued"  # queued, running, completed, failed, cancelled
    progress: float = 0.0
    message: str = ""
    created: float = field(default_factory=time)
    started: float | None = None
    finished: float | None = None
    result: Any = None
    error: str | None = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
            "created": self.created,
            "started": self.started,
            "finished": self.finished,
            "result": self.result,
            "error": self.error,
        }
