import { useState } from "react";
import API from "../api/client";

// ✅ CLEAN URL (NO embed!)
const getCleanUrl = (url) => {
  try {
    const parsed = new URL(url);

    if (parsed.hostname.includes("youtube.com")) {
      const videoId = parsed.searchParams.get("v");
      return videoId
        ? `https://www.youtube.com/watch?v=${videoId}`
        : url;
    }

    if (parsed.hostname.includes("youtu.be")) {
      const videoId = parsed.pathname.replace("/", "");
      return `https://www.youtube.com/watch?v=${videoId}`;
    }

    return url;
  } catch {
    return url;
  }
};

export default function UrlInput({ onProcessed }) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleProcess = async () => {
    if (!url.trim()) return alert("Please enter a URL");

    setLoading(true);
    try {
      const cleanUrl = getCleanUrl(url.trim());

      console.log("✅ CLEAN URL:", cleanUrl);

      const res = await API.post("/ingest/url", { url: cleanUrl });

      onProcessed({
        jobId: res.data.job_id,
        videoId: res.data.video_id,
        videoUrl: cleanUrl, // ✅ WATCH URL
      });
    } catch (error) {
      console.error(error);
      alert("Failed to process video");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Paste YouTube URL..."
        style={styles.input}
      />
      <button onClick={handleProcess} style={styles.button}>
        {loading ? "Processing..." : "Process Video"}
      </button>
    </div>
  );
}

const styles = {
  container: { display: "flex", gap: "10px" },
  input: { flex: 1, padding: "10px" },
  button: { padding: "10px" },
};