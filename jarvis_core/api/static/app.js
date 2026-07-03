async function getJSON(url) {
  const res = await fetch(url);
  return await res.json();
}

function pretty(obj) {
  return JSON.stringify(obj, null, 2);
}

async function refreshHealth() {
  try {
    const data = await getJSON('/health');
    document.getElementById('health').textContent = 'Online';
  } catch {
    document.getElementById('health').textContent = 'Offline';
  }
}

async function refreshStatus() {
  const res = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: 'How healthy is my AI server?'})
  });
  const data = await res.json();
  document.getElementById('statusBox').textContent =
    data.response || pretty(data);
}

async function refreshSkills() {
  const data = await getJSON('/skills');
  document.getElementById('skillsBox').textContent = pretty(data);
}

async function refreshActions() {
  const data = await getJSON('/actions');
  document.getElementById('actionsBox').textContent = pretty(data);
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
  addMsg('jarvis', data.response || pretty(data));
  refreshActions();
}

document.getElementById('chatInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') sendChat();
});

refreshHealth();
refreshStatus();
refreshSkills();
refreshActions();
setInterval(refreshHealth, 10000);
