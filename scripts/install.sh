#!/bin/bash
set -e

BASE="$HOME/jarvis"

mkdir -p "$BASE"
cp -r . "$BASE"

cd "$BASE"
cp -n config/settings.env.example config/settings.env

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sudo tee /etc/systemd/system/jarvis.service > /dev/null <<EOF
[Unit]
Description=Jarvis v1 Local AI Agent
After=network-online.target ollama.service docker.service
Wants=network-online.target

[Service]
User=ubuntuai
WorkingDirectory=/home/ubuntuai/jarvis
EnvironmentFile=/home/ubuntuai/jarvis/config/settings.env
ExecStart=/home/ubuntuai/jarvis/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 5050
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable jarvis
sudo systemctl restart jarvis

echo "Jarvis v1 installed."
echo "Test: curl http://127.0.0.1:5050/health"
