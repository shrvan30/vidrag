import { useState } from "react";
import API from "../api/client";

export default function SearchBar({ videoId, setResults, setLoading }) {
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  const search = async () => {
    const trimmed = query.trim();

    if (!trimmed) {
      setError("⚠️ Enter a query");
      return;
    }

    if (!videoId) {
      setError("⚠️ Process video first");
      return;
    }

    try {
      setError("");
      setLoading(true);

      const res = await API.post("/search", {
        query: trimmed,
        video_id: videoId,
      });

      const searchResults = res.data?.results || [];

      if (searchResults.length === 0) {
        setError("⚠️ No results found");
      }

      setResults(searchResults);

    } catch (err) {
      console.error(err);
      setError("Search failed");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <input
        placeholder="Search inside video..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && search()}
        style={{ padding: "10px", width: "60%" }}
      />

      <button onClick={search} disabled={!videoId}>
        Search
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}