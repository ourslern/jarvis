import { useEffect, useState } from "react";
import { getLiveStatus, directDockerAction, getDockerLogs } from "../api/jarvis";
import { Card } from "../components/Card";
import { Header } from "../components/layout/Header";

export function Containers() {
  const [live, setLive] = useState<any>(null);
  const [output, setOutput] = useState("");

  async function refresh() {
    setLive(await getLiveStatus());
  }

  async function run(action: string, name: string) {
    setOutput(`Running ${action} on ${name}...`);

    if (action === "logs") {
      const res = await getDockerLogs(name);
      setOutput(res.logs || JSON.stringify(res, null, 2));
    } else {
      const res = await directDockerAction(action, name);
      setOutput(JSON.stringify(res, null, 2));
    }

    refresh();
  }

  useEffect(() => {
    refresh();
    const t = setInterval(refresh, 5000);
    return () => clearInterval(t);
  }, []);

  return (
    <>
      <Header title="Containers" subtitle="Docker services running on your AI server" />

      <section className="container-grid">
        {live?.docker?.containers?.map((c: any) => (
          <div key={c.name} className="container-card">
            <div>
              <h2>{c.name}</h2>
              <p>{c.image}</p>
            </div>

            <div className={c.status === "running" ? "badge green" : "badge gray"}>
              {c.status === "running" ? "Running" : c.status}
            </div>

            <div className="button-row">
              <button onClick={() => run("restart", c.name)}>Restart</button>
              {c.status === "running" ? (
                <button onClick={() => run("stop", c.name)}>Stop</button>
              ) : (
                <button onClick={() => run("start", c.name)}>Start</button>
              )}
              <button onClick={() => run("logs", c.name)}>Logs</button>
            </div>
          </div>
        ))}
      </section>

      <Card title="Output" className="chat-card">
        <pre>{output || "No action yet."}</pre>
      </Card>
    </>
  );
}
