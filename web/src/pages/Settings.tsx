import { Header } from "../components/layout/Header";
import { Card } from "../components/Card";

export function Settings() {
  return (
    <>
      <Header title="Settings" subtitle="Jarvis configuration" />

      <section className="grid">
        <Card title="System">
          <p>Jarvis 3 backend: http://127.0.0.1:5051</p>
          <p>React UI: http://localhost:5173</p>
        </Card>

        <Card title="Status">
          <p>Settings page is online.</p>
          <p>Configuration controls will be added later.</p>
        </Card>
      </section>
    </>
  );
}
