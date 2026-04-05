import { useEffect, useState } from "react";

export default function useWebSocket(jobId) {
  const [status, setStatus] = useState("");

  useEffect(() => {
    if (!jobId) return;

    const ws = new WebSocket(`ws://localhost:8000/ws/job/${jobId}`);

    ws.onmessage = (event) => {
      setStatus(event.data);
    };

    ws.onerror = () => {
      setStatus("Error connecting...");
    };

    return () => ws.close();
  }, [jobId]);

  return status;
}