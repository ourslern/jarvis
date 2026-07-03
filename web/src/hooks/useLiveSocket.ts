import { useEffect, useState } from "react";

export function useLiveSocket() {
  const [live, setLive] = useState<any>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:5051/ws/live");

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onerror = () => setConnected(false);

    ws.onmessage = (event) => {
      setLive(JSON.parse(event.data));
    };

    return () => ws.close();
  }, []);

  return { live, connected };
}
