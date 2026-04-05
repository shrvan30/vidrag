import { useState, useRef, useEffect } from "react";

export default function ChatBox({ videoId }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const controllerRef = useRef(null);
  const answerRef = useRef("");

  useEffect(() => {
    return () => {
      controllerRef.current?.abort();
    };
  }, []);

  const cleanText = (text) => {
    return text
      .replace(/<\|.*?\|>/g, "")
      .replace(/Answer:/gi, "")
      .replace(/\n{2,}/g, "\n")
      .trim();
  };

  const askQuestion = async () => {
    if (!question.trim() || !videoId) return;

    setAnswer("");
    answerRef.current = "";
    setLoading(true);

    controllerRef.current?.abort();

    const controller = new AbortController();
    controllerRef.current = controller;

    try {
      const response = await fetch("http://localhost:8000/qa", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          video_id: videoId,
        }),
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        if (!chunk) continue;

        answerRef.current += chunk;
        setAnswer(cleanText(answerRef.current));
      }

    } catch (err) {
      if (err.name !== "AbortError") {
        console.error("❌ QA Error:", err);
        setAnswer("❌ Failed to get answer");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>🤖 Ask AI about this video</h3>

      <div style={styles.inputRow}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && askQuestion()}
          placeholder="Ask anything from video..."
          style={styles.input}
        />

        <button
          onClick={askQuestion}
          disabled={loading || !videoId || !question.trim()}
          style={styles.button}
        >
          {loading ? "..." : "Ask"}
        </button>
      </div>

      <div style={styles.answer}>
        {loading && !answer
          ? "⏳ Thinking..."
          : answer || "💬 Ask something..."}
      </div>
    </div>
  );
}

const styles = {
  container: {
    marginTop: "30px",
  },
  title: {
    marginBottom: "10px",
  },
  inputRow: {
    display: "flex",
    gap: "10px",
  },
  input: {
    flex: 1,
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #334155",
    outline: "none",
  },
  button: {
    padding: "12px 18px",
    background: "#38bdf8",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    color: "black",
    fontWeight: "bold",
  },
  answer: {
    marginTop: "15px",
    padding: "15px",
    background: "#1e293b",
    borderRadius: "10px",
    minHeight: "80px",
    whiteSpace: "pre-wrap",
    lineHeight: "1.5",
  },
};