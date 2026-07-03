import { Header } from "../components/layout/Header";
import { useLiveHistory } from "../hooks/useLiveHistory";
import { LiveLineChart } from "../components/charts/LiveLineChart";

export function Performance() {
  const history = useLiveHistory();

  return (
    <>
      <Header title="Performance" subtitle="Live CPU, RAM, GPU, VRAM, temperature, and power history" />

      <section className="grid">
        <LiveLineChart title="CPU" data={history} dataKey="cpu" suffix="%" />
        <LiveLineChart title="RAM" data={history} dataKey="ram" suffix="%" />
        <LiveLineChart title="GPU" data={history} dataKey="gpu" suffix="%" />
        <LiveLineChart title="VRAM" data={history} dataKey="vram" suffix="%" />
        <LiveLineChart title="GPU Temperature" data={history} dataKey="temp" suffix="°C" />
        <LiveLineChart title="GPU Power" data={history} dataKey="power" suffix=" W" />
      </section>
    </>
  );
}
