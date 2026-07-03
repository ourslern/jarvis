import { useEffect } from "react";

export function useJobsSocket(onUpdate: (job: any) => void) {
    useEffect(() => {

        const ws = new WebSocket("ws://localhost:5051/ws/jobs");

        ws.onmessage = (event) => {

            const data = JSON.parse(event.data);

            if (data.event === "job.updated") {
                onUpdate(data.payload);
            }
        };

        return () => ws.close();

    }, []);
}

