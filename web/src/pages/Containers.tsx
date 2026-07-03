import { useEffect, useState } from "react";
import { getLiveStatus } from "../api/jarvis";
import { Card } from "../components/Card";
import { Header } from "../components/layout/Header";
import { ContainerList } from "../components/ContainerList";

export function Containers() {
  const [live, setLive] = useState<any>(null);

  useEffect(() => {
    getLiveStatus().then(setLive);
  }, []);

  return (
    <>
      <Header title="Containers" subtitle="Docker services running on your AI server" />
      <Card title={`${live?.docker?.running ?? 0} / ${live?.docker?.total ?? 0} running`}>
        <ContainerList containers={live?.docker?.containers || []} />
      </Card>
    </>
  );
}
