import { useEffect, useState } from "react";
import { getLiveStatus } from "../api/jarvis";

export function useLiveHistory(maxPoints = 60) {
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    let active = true;

    async function tick() {
      const data = await getLiveStatus();
      const gpu = data.gpu;
      const sys = data.system;

      const point = {
        time: new Date().toLocaleTimeString(),
        cpu: sys.cpu_percent,
        ram: sys.ram_percent,
        gpu: gpu.util_percent,
        vram: gpu.memory_total_mb ? (gpu.memory_used_mb / gpu.memory_total_mb) * 100 : 0,
        temp: gpu.temperature_c,
        power: gpu.power_watts,
      };

      if (active) {
        setHistory((h) => [...h.slice(-(maxPoints - 1)), point]);
      }
    }

    tick();
    const interval = setInterval(tick, 3000);

    return () => {
      active = false;
      clearInterval(interval);
    };
  }, [maxPoints]);

  return history;
}
