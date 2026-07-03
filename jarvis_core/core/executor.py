from jarvis_core.core.permissions import requires_confirmation

def execute_plan(decision: dict, registry, confirmed: bool = False) -> dict:
    results = []
    for step in decision.get("steps", []):
        action_name = step.get("action")
        args = step.get("args", {}) or {}
        action = registry.actions.get(action_name)
        if action is None:
            results.append({"action": action_name, "success": False, "error": "Unknown action", "step": step})
            continue
        if requires_confirmation(action.permission) and not confirmed:
            results.append({
                "action": action_name,
                "success": False,
                "skipped": True,
                "requires_confirmation": True,
                "reason": "Confirmation required before running this action.",
                "step": step,
            })
            continue
        try:
            result = registry.run(action_name, **args)
            results.append({"action": action_name, "args": args, "success": True, "result": result})
        except Exception as e:
            results.append({"action": action_name, "args": args, "success": False, "error": str(e)})
    return {"decision": decision, "results": results}
