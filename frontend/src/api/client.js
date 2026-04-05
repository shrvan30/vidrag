import axios from "axios";

// Create Axios instance with base URL
const API = axios.create({
  baseURL: "http://localhost:8000", // ✅ correct (gateway)
  headers: {
    "Content-Type": "application/json",
  },
});

// Export the Axios instance as default
export default API;

// ✅ FIX 1: Correct endpoint
export async function processVideo(url) {
  const res = await fetch("http://localhost:8000/ingest/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  return res.json();
}

// ✅ FIX 2: Correct field name
export async function searchQuery(query, video_id) {
  const res = await fetch("http://localhost:8000/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, video_id }),
  });
  return res.json();
}