import json
import re

from app.ollama import chat
from app.tool_registry import list_tools, run_tool


def _extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except Exception:
        return None


def choose_tools(message: str, model: str | None = None) -> dict:
    tools = list_tools()

    prompt = f"""
You are Jarvis' tool decision engine.

User request:
{message}

Available tools:
{json.dumps(tools, indent=2)}

Choose which tools to run.

Rules:
- Only use tools from the available tools list.
- For read_only=false tools, set requires_confirmation=true.
- If no tool is needed, return an empty steps list.
- Return ONLY valid JSON.

JSON format:
{{
  "goal": "short goal",
  "steps": [
    {{
      "tool": "tool.name",
      "args": {{}},
      "reason": "why this tool is needed",
      "requires_confirmation": false
    }}
  ]
}}
"""

    response = chat(prompt, model=model)
    parsed = _extract_json(response)

    if not parsed:
        return {
            "goal": "Unable to parse tool decision",
            "steps": [],
            "raw_model_response": response,
        }

    return parsed


def execute_decision(decision: dict) -> dict:
    results = []

    for step in decision.get("steps", []):
        if step.get("requires_confirmation"):
            results.append({
                "tool": step.get("tool"),
                "skipped": True,
                "reason": "Confirmation required before running write/action tool.",
                "step": step,
            })
            continue

        tool_name = step.get("tool")
        args = step.get("args", {}) or {}

        try:
            result = run_tool(tool_name, **args)
            results.append({
                "tool": tool_name,
                "args": args,
                "result": result,
                "success": True,
            })
        except Exception as e:
            results.append({
                "tool": tool_name,
                "args": args,
                "error": str(e),
                "success": False,
            })

    return {
        "decision": decision,
        "results": results,
    }
