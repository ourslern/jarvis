async function getJSON(url) {
  const res = await fetch(url);
  return await res.json();
}

function setRing(id, value) {
  const el = document.getElementById(id);
  const v = Math.max(0, Math.min(100, Number(value || 0)));
  el.parentElement.style.setProperty('--value', `${v}%`);
  el.textContent = `${v.toFixed(0)}%`;
}

async function refreshLive() {
  const data = await getJSON('/dashboard/live');

  const sys = data.system;
  const gpu = data.gpu;
  const vramPct = gpu.memory_total_mb
    ? (gpu.memory_used_mb / gpu.memory_total_mb) * 100
    : 0;

  setRing('cpuValue', sys.cpu_percent);
  setRing('ramValue', sys.ram_percent);
  setRing('gpuValue', gpu.util_percent);
  setRing('vramValue', vramPct);

  document.getElementById('gpuBox').textContent =
`GPU: ${gpu.name}
Load: ${gpu.util_percent}%
VRAM: ${gpu.memory_used_mb} / ${gpu.memory_total_mb} MB
Temp: ${gpu.temperature_c}°C
Power: ${gpu.power_watts} W

Jarvis:
PID: ${data.jarvis.pid}
Uptime: ${data.jarvis.uptime_minutes} min
Memory: ${data.jarvis.memory_mb} MB`;

  document.getElementById('dockerBox').textContent =
`Running: ${data.docker.running} / ${data.docker.total}

${data.docker.containers.map(c => `${c.status === 'running' ? '🟢' : '⚪'} ${c.name}`).join('\n')}`;
}


async function refreshModels() {
  const data = await getJSON('/dashboard/models');

  const installed = data.models
    .map(m => `○ ${m.name} — ${m.size_gb} GB`)
    .join('\n');

  const running = data.running?.length
    ? data.running.map(m => `● ${m.name} — ${(m.size_vram / 1024 / 1024 / 1024).toFixed(2)} GB VRAM`).join('\n')
    : 'No models currently running.';

  document.getElementById('modelsBox').textContent =
`Running Models:
${running}

Installed Models:
${installed}`;
}

async function refreshActions() {
  const data = await getJSON('/dashboard/jarvis');
  document.getElementById('actionsBox').textContent =
    data.recent_actions.map(a => `• ${a.action} (${a.duration_sec}s)`).join('\n') || 'No recent actions.';
}

async function refreshHealth() {
  try {
    await getJSON('/health');
    document.getElementById('health').textContent = 'Online';
  } catch {
    document.getElementById('health').textContent = 'Offline';
  }
}

function addMsg(role, text) {
  const log = document.getElementById('chatLog');
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.textContent = text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

async function sendChat() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  if (!message) return;

  addMsg('user', message);
  input.value = '';

  const res = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message})
  });

  const data = await res.json();
  addMsg('jarvis', data.response || JSON.stringify(data, null, 2));
  refreshActions();
refreshModels();
}

document.getElementById('chatInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') sendChat();
});

refreshHealth();
refreshLive();
refreshActions();

setInterval(refreshHealth, 10000);
setInterval(refreshLive, 3000);
setInterval(refreshActions, 8000);
setInterval(refreshModels, 10000);
