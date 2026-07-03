import { useEffect, useState } from "react";
import { getModels } from "../api/jarvis";
import { Card } from "../components/Card";
import { Header } from "../components/layout/Header";
import { ModelList } from "../components/ModelList";

export function Models() {
  const [models, setModels] = useState<any>(null);

  useEffect(() => {
    getModels().then(setModels);
  }, []);

  return (
    <>
      <Header title="Models" subtitle="Installed and running Ollama models" />
      <section className="grid">
        <Card title="Running Models">
          <ModelList models={models?.running || []} />
        </Card>
        <Card title="Installed Models">
          <ModelList models={models?.models || []} />
        </Card>
      </section>
    </>
  );
}
