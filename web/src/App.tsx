import { useEffect, useState } from "react";
import { Cpu, HardDrive, Bot, Activity } from "lucide-react";
import { getLiveStatus, getModels, askJarvis } from "./api/jarvis";
import { MetricCard } from "./components/MetricCard";
import { Card } from "./components/Card";
import { ContainerList } from "./components/ContainerList";
import { ModelList } from "./components/ModelList";
import "./App.css";

export default function App() {
  const [live, setLive] = useState<any>(null);
  const [models, setModels] = useState<any>(null);
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState<string[]>([]);

  async function refresh() {
    setLive(await getLiveStatus());
    setModels(await getModels());
  }

  async function send() {
    if (!message.trim()) return;
    const msg = message.trim();
    setChat((c) => [...c, `You: ${msg}`]);
    setMessage("");

    const res = await askJarvis(msg);
    setChat((c) => [...c, `Jarvis: ${res.response || JSON.stringify(res)}`]);
  }

  useEffect(() => {
    refresh();
    const t = setInterval(refresh, 3000);
    return () => clearInterval(t);
  }, []);

  const gpu = live?.gpu;
  const sys = live?.system;
  const docker = live?.docker;

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">JARVIS</div>
        <div className="tag">Local AI OS</div>
        <nav>
          <button>Dashboard</button>
          <button>Models</button>
          <button>Containers</button>
          <button>Chat</button>
        </nav>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h1>AI Control Center</h1>
            <p>Ubuntu · RTX 3080 Ti · Ollama · SearXNG</p>
          </div>
          <div className="status-pill">Online</div>
        </header>

        <section className="metrics">
          <MetricCard title="CPU" value={`${sys?.cpu_percent ?? 0}%`} subtitle="System load" icon={<Cpu />} />
          <MetricCard title="RAM" value={`${sys?.ram_percent ?? 0}%`} subtitle="Memory usage" icon={<Activity />} />
          <MetricCard title="GPU" value={`${gpu?.util_percent ?? 0}%`} subtitle={`${gpu?.temperature_c ?? 0}°C`} icon={<Bot />} />
          <MetricCard title="Disk" value={`${sys?.disk_percent ?? 0}%`} subtitle="Storage used" icon={<HardDrive />} />
        </section>

        <section className="grid">
          <Card title="GPU">
            <p>{gpu?.name}</p>
            <p>VRAM: {gpu?.memory_used_mb} / {gpu?.memory_total_mb} MB</p>
            <p>Power: {gpu?.power_watts} W</p>
          </Card>

          <Card title="Containers">
            <p>{docker?.running} / {docker?.total} running</p>
            <ContainerList containers={docker?.containers || []} />
          </Card>

          <Card title="Models">
            <ModelList models={models?.models || []} />
          </Card>

          <Card title="Chat" className="chat-card">
            <div className="chat-log">
              {chat.map((line, i) => <div key={i}>{line}</div>)}
            </div>
            <div className="chat-input">
              <input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && send()}
                placeholder="Ask Jarvis..."
              />
              <button onClick={send}>Send</button>
            </div>
          </Card>
        </section>
      </main>
    </div>
  );
}
