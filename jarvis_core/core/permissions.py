from jarvis_core.core.types import PermissionLevel

def requires_confirmation(permission: PermissionLevel) -> bool:
    return permission in {PermissionLevel.SAFE_WRITE, PermissionLevel.DANGEROUS}
