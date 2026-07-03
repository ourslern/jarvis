#!/bin/bash
cd "$(dirname "$0")/.."
source venv/bin/activate
uvicorn jarvis_core.api.server:app --host 0.0.0.0 --port 5051
