import { useState, useCallback } from "react";

import UrlInput from "./components/UrlInput";
import ProgressBar from "./components/ProgressBar";
import SearchBar from "./components/SearchBar";
import VideoPlayer from "./components/VideoPlayer";
import ResultsList from "./components/ResultsList";
import ChatBox from "./components/ChatBox";

function App() {
  const [jobId, setJobId] = useState(null);
  const [videoId, setVideoId] = useState(null);
  const [videoUrl, setVideoUrl] = useState("");

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const [seekTime, setSeekTime] = useState(null);
  const [currentTime, setCurrentTime] = useState(0);

  const handleProcessed = useCallback(({ jobId, videoId, videoUrl }) => {
    setJobId(jobId);
    setVideoId(videoId);
    setVideoUrl(videoUrl);
    setResults([]);
    setSeekTime(null);
  }, []);

  const handleSeek = useCallback((time) => {
    setSeekTime(time);
  }, []);

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🎬 VidRAG AI</h1>

      {/* URL INPUT */}
      <UrlInput onProcessed={handleProcessed} />

      {/* STATUS */}
      {!videoId && !jobId && (
        <p style={styles.centerText}>
          🎥 Paste a YouTube URL and click <b>Process</b>
        </p>
      )}

      {jobId && !videoId && (
        <p style={styles.processing}>⚙️ Processing video...</p>
      )}

      {videoId && <p style={styles.ready}>✅ Ready for search</p>}

      {jobId && <ProgressBar jobId={jobId} />}

      {/* SEARCH */}
      <SearchBar
        videoId={videoId}
        setResults={setResults}
        setLoading={setLoading}
      />

      {loading && <p style={styles.centerText}>🔄 Searching...</p>}

      {/* MAIN LAYOUT */}
      <div style={styles.mainGrid}>
        {/* LEFT → VIDEO */}
        <div style={styles.videoSection}>
          <VideoPlayer
            url={videoUrl}
            seekTo={seekTime}
            onTimeUpdate={setCurrentTime}
          />
        </div>

        {/* RIGHT → RESULTS */}
        <div style={styles.resultsSection}>
          <h3 style={styles.sectionTitle}>📄 Results</h3>
          <ResultsList
            results={results}
            onSelect={handleSeek}
            currentTime={currentTime}
          />
        </div>
      </div>

      {/* AI ANSWER */}
      {results.length > 0 && (
        <div style={styles.answerBox}>
          <h3>🧠 Quick Insight</h3>
          <p>
            {results[0]?.text ??
              results[0]?.context ??
              "No answer available"}
          </p>
        </div>
      )}

      {/* CHAT */}
      <ChatBox videoId={videoId} />
    </div>
  );
}

export default App;

const styles = {
  container: {
    padding: "20px",
    maxWidth: "1300px",
    margin: "auto",
    background: "#0f172a",
    minHeight: "100vh",
    color: "white",
  },

  title: {
    textAlign: "center",
    color: "#38bdf8",
    marginBottom: "20px",
  },

  centerText: {
    textAlign: "center",
    color: "gray",
  },

  processing: {
    textAlign: "center",
    color: "#facc15",
  },

  ready: {
    textAlign: "center",
    color: "#22c55e",
  },

  mainGrid: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "20px",
    marginTop: "25px",
    alignItems: "start",
  },

  videoSection: {
    background: "#020617",
    padding: "10px",
    borderRadius: "10px",
  },

  resultsSection: {
    background: "#020617",
    padding: "10px",
    borderRadius: "10px",
    maxHeight: "500px",
    overflow: "hidden",
  },

  sectionTitle: {
    marginBottom: "10px",
    color: "#38bdf8",
  },

  answerBox: {
    marginTop: "25px",
    background: "#020617",
    padding: "15px",
    borderRadius: "10px",
    border: "1px solid #38bdf8",
  },
};