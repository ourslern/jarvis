from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any

class PermissionLevel(str, Enum):
    READ = "read"
    SAFE_WRITE = "safe_write"
    DANGEROUS = "dangerous"

@dataclass
class Action:
    name: str
    description: str
    permission: PermissionLevel
    function: Callable[..., Any]
    args_schema: dict | None = None
