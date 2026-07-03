#!/bin/bash
set -e
curl http://127.0.0.1:5051/health
echo
curl http://127.0.0.1:5051/skills
echo
curl -X POST http://127.0.0.1:5051/chat -H "Content-Type: application/json" -d '{"message":"How healthy is my AI server?"}'
echo
