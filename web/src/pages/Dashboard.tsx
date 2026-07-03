import { useEffect, useState } from "react";
import { Cpu, HardDrive, Bot, Activity } from "lucide-react";
import { getLiveStatus, getModels } from "../api/jarvis";
import { MetricCard } from "../components/MetricCard";
import { Card } from "../components/Card";
import { ContainerList } from "../components/ContainerList";
import { ModelList } from "../components/ModelList";
import { Header } from "../components/layout/Header";

export function Dashboard() {
  const [live, setLive] = useState<any>(null);
  const [models, setModels] = useState<any>(null);

  async function refresh() {
    setLive(await getLiveStatus());
    setModels(await getModels());
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
    <>
      <Header title="AI Control Center" subtitle="Ubuntu · RTX 3080 Ti · Ollama · SearXNG" />

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
      </section>
    </>
  );
}
