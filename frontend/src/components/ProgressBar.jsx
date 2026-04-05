import { useEffect, useState } from "react";

export default function ProgressBar({ jobId }) {
  const [status, setStatus] = useState("");

  useEffect(() => {
    if (!jobId) return;

    const ws = new WebSocket(`ws://localhost:8000/ws/job/${jobId}`);

    ws.onmessage = (event) => {
      setStatus(event.data);
    };

    ws.onerror = () => {
      setStatus("Connection error");
    };

    return () => ws.close();
  }, [jobId]);

  if (!jobId) return null;

  return (
    <div style={{ marginTop: "10px" }}>
      <b>Status:</b> {status || "Starting..."}
    </div>
  );
}