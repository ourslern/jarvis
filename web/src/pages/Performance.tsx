import { Header } from "../components/layout/Header";
import { Card } from "../components/Card";

export function Performance() {
  return (
    <>
      <Header title="Performance" subtitle="Live charts coming next" />
      <Card title="Charts">
        <p>Next step: CPU, RAM, GPU, VRAM, temperature, and power charts.</p>
      </Card>
    </>
  );
}
