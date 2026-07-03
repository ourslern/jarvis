import json, re
from jarvis_core.core.ollama import chat

def _extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except Exception:
        return None

def choose_actions(message: str, available_actions: list[dict], model: str | None = None) -> dict:
    prompt = f"""
You are Jarvis' decision engine.

User request:
{message}

Available actions:
{json.dumps(available_actions, indent=2)}

Choose actions to satisfy the request.

Rules:
- Only choose actions from the available actions list.
- Prefer read actions for diagnosing.
- For safe_write or dangerous actions, include requires_confirmation=true.
- If no action is needed, return steps: [].
- Return ONLY valid JSON.

JSON format:
{{
  "goal": "short goal",
  "steps": [
    {{
      "action": "action.name",
      "args": {{}},
      "reason": "why this action is needed",
      "requires_confirmation": false
    }}
  ]
}}
"""
    response = chat(prompt, model=model)
    parsed = _extract_json(response)
    return parsed or {"goal": "Unable to parse model decision", "steps": [], "raw_model_response": response}
