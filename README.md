# Jarvis v1

Persistent local AI assistant for Nate's Ubuntu AI PC.

## Features

- Persistent FastAPI service
- Ollama chat endpoint
- SearXNG web search endpoint
- System and GPU status
- Docker container status and restart
- Safe workspace file access
- Simple JSON memory

## Install

```bash
unzip jarvis-v1.zip
cd jarvis-v1
chmod +x scripts/install.sh scripts/test.sh
./scripts/install.sh
```

## Test

```bash
curl http://127.0.0.1:5050/health
curl http://127.0.0.1:5050/status
curl http://127.0.0.1:5050/docker
curl "http://127.0.0.1:5050/search?q=open%20webui"
```

## Chat

```bash
curl -X POST http://127.0.0.1:5050/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"How is the AI server doing?"}'
```

## Built-in command examples

- `system status`
- `docker status`
- `search latest Open WebUI release`
- `list files`
- `write file notes/test.md: hello from Jarvis`
- `read file notes/test.md`
- `remember favorite_model: qwen3:14b`
- `recall favorite_model`
