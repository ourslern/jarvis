const API_BASE = "http://127.0.0.1:5051";

export async function getLiveStatus() {
  const res = await fetch(`${API_BASE}/dashboard/live`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getModels() {
  const res = await fetch(`${API_BASE}/api/ollama/overview`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function askJarvis(message: string) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message}),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function directDockerAction(action: string, name: string) {
  const res = await fetch(`${API_BASE}/api/docker/${action}/${name}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getDockerLogs(name: string) {
  const res = await fetch(`${API_BASE}/api/docker/logs/${name}?lines=120`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function ollamaAction(action: string, model: string) {
  const res = await fetch(
    `${API_BASE}/api/ollama/${action}/${encodeURIComponent(model)}`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function pullModelJob(model: string) {
  const res = await fetch(
    `${API_BASE}/api/jobs/ollama/pull/${encodeURIComponent(model)}`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getJobs() {
  const res = await fetch(`${API_BASE}/api/jobs`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
