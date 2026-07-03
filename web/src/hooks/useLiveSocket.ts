import { useEffect, useState } from "react";
import { getLiveStatus } from "../api/jarvis";

export function useLiveSocket() {
  const [live, setLive] = useState<any>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    getLiveStatus().then(setLive).catch(console.error);

    const ws = new WebSocket("ws://localhost:5051/ws/live");

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onerror = () => setConnected(false);

    ws.onmessage = (event) => {
      setLive(JSON.parse(event.data));
    };

    const fallback = setInterval(() => {
      getLiveStatus().then(setLive).catch(console.error);
    }, 5000);

    return () => {
      clearInterval(fallback);
      ws.close();
    };
  }, []);

  return { live, connected };
}
