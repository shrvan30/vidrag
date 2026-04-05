import { useRef, useEffect } from "react";

export default function ResultsList({ results, onSelect, currentTime }) {
  const activeRef = useRef(null);

  // ✅ Auto-scroll active item
  useEffect(() => {
    if (activeRef.current) {
      activeRef.current.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }
  }, [currentTime]);

  // ✅ Time formatter (mm:ss / hh:mm:ss)
  const formatTime = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, "0")}:${secs
        .toString()
        .padStart(2, "0")}`;
    }

    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  if (!results || results.length === 0) {
    return <p style={{ color: "gray" }}>No results</p>;
  }

  return (
    <div style={styles.container}>
      {results.map((r, i) => {
        const start = r.start ?? r.start_s ?? 0;
        const end = r.end ?? start + 5;

        const text =
          r.text ?? r.context ?? r.content ?? "No content available";

        const isActive =
          currentTime >= start && currentTime <= end;

        return (
          <div
            key={i}
            ref={isActive ? activeRef : null}
            onClick={() => onSelect(start)}
            style={{
              ...styles.card,
              border: isActive
                ? "2px solid #38bdf8"
                : "1px solid #1e293b",
              background: isActive ? "#1e293b" : "#020617",
              transform: isActive ? "scale(1.02)" : "scale(1)",
            }}
          >
            {/* ⏱ Timestamp */}
            <div style={styles.time}>
              ⏱ {formatTime(start)} - {formatTime(end)}
            </div>

            {/* 📄 Text */}
            <p style={styles.text}>{text}</p>
          </div>
        );
      })}
    </div>
  );
}

const styles = {
  container: {
    maxHeight: "420px",
    overflowY: "auto",
    paddingRight: "6px",
  },
  card: {
    padding: "12px",
    marginBottom: "10px",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "all 0.2s ease",
  },
  time: {
    color: "#38bdf8",
    fontWeight: "bold",
    fontSize: "14px",
  },
  text: {
    marginTop: "6px",
    lineHeight: "1.4",
    fontSize: "14px",
  },
};