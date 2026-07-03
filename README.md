# Jarvis 3 — Milestone 1

Clean architecture rebuild for Jarvis.

## Install

```bash
cp -r jarvis3-m1/* ~/jarvis/
cd ~/jarvis
source venv/bin/activate
pip install -r requirements.txt
```

## Run alongside Jarvis v2

```bash
uvicorn jarvis_core.api.server:app --host 0.0.0.0 --port 5051
```

## Test

```bash
curl http://127.0.0.1:5051/health
curl http://127.0.0.1:5051/skills
curl -X POST http://127.0.0.1:5051/chat -H "Content-Type: application/json" -d '{"message":"How healthy is my AI server?"}'
```
