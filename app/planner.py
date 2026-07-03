from app.tool_registry import run_tool

# Register tools
import app.tools.system
import app.tools.docker_tool
import app.tools.websearch
import app.tools.filesystem

def make_plan(message: str) -> list[dict]:
    m = message.lower().strip()
    plan = []

    if "ai server" in m or "server health" in m or "system health" in m:
        plan.append({"tool": "system.status", "args": {}})
        plan.append({"tool": "docker.containers", "args": {}})

    elif "open webui" in m and ("status" in m or "health" in m):
        plan.append({"tool": "docker.containers", "args": {}})
        plan.append({"tool": "web.search", "args": {"query": "Open WebUI latest release", "limit": 3}})

    elif "search" in m:
        q = m.replace("search", "", 1).strip()
        plan.append({"tool": "web.search", "args": {"query": q}})

    return plan


def run_plan(plan: list[dict]) -> list[dict]:
    results = []

    for step in plan:
        tool_name = step["tool"]
        args = step.get("args", {})
        result = run_tool(tool_name, **args)
        results.append({
            "tool": tool_name,
            "args": args,
            "result": result,
        })

    return results
