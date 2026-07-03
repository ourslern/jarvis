const API_BASE = "http://127.0.0.1:5051";

export async function getLiveStatus() {
  const res = await fetch(`${API_BASE}/dashboard/live`);
  return res.json();
}

export async function getModels() {
  const res = await fetch(`${API_BASE}/dashboard/models`);
  return res.json();
}

export async function askJarvis(message: string) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message}),
  });
  return res.json();
}
