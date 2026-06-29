#!/bin/bash
set -e

curl http://127.0.0.1:5050/health
echo
curl http://127.0.0.1:5050/status
echo
curl http://127.0.0.1:5050/docker
echo
curl "http://127.0.0.1:5050/search?q=open%20webui"
echo
curl -X POST http://127.0.0.1:5050/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"How is the AI server doing?"}'
echo
