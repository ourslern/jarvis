import { useEffect, useState } from "react";
import { getModels } from "../api/jarvis";
import { useLiveSocket } from "../hooks/useLiveSocket";
import { StatusBar } from "../components/layout/StatusBar";
import { GaugeCard } from "../components/GaugeCard";
import { Card } from "../components/Card";
import { ContainerList } from "../components/ContainerList";
import { ModelList } from "../components/ModelList";
import { Header } from "../components/layout/Header";

export function Dashboard() {
  const { live, connected } = useLiveSocket();
  const [models, setModels] = useState<any>(null);

  useEffect(() => {
    getModels().then(setModels);
  }, []);

  const gpu = live?.gpu;
  const sys = live?.system;
  const docker = live?.docker;

  return (
    <>
      <Header title="AI Control Center" subtitle="Ubuntu · RTX 3080 Ti · Ollama · SearXNG" />

      <StatusBar live={live} connected={connected} />

      <section className="metrics">
        <GaugeCard title="CPU" value={sys?.cpu_percent ?? 0} subtitle="Load" detail="System processor" />
        <GaugeCard title="RAM" value={sys?.ram_percent ?? 0} subtitle="Memory" detail="System memory" />
        <GaugeCard title="GPU" value={gpu?.util_percent ?? 0} subtitle="Load" detail={`${gpu?.temperature_c ?? 0}°C · ${gpu?.power_watts ?? 0} W`} />
        <GaugeCard title="VRAM" value={gpu?.memory_total_mb ? (gpu.memory_used_mb / gpu.memory_total_mb) * 100 : 0} subtitle="VRAM" detail={`${gpu?.memory_used_mb ?? 0} / ${gpu?.memory_total_mb ?? 0} MB`} />
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
