import os


# =========================
# 🔍 SEARCH CONFIG
# =========================
# Internal Docker service name (correct)
SEARCH_URL = os.getenv("SEARCH_URL", "http://search:8003/search")

# Number of chunks retrieved from search
TOP_K = int(os.getenv("TOP_K", 3))


# =========================
# 🧠 CONTEXT CONTROL
# =========================
# Number of chunks passed to LLM (keep small for speed)
CONTEXT_LIMIT = int(os.getenv("CONTEXT_LIMIT", 5))


# =========================
# 🤖 LLM CONFIG
# =========================
# ✅ FIXED: correct llama.cpp endpoint
LLM_URL = os.getenv("LLM_URL", "http://llm:8080/completion")

# 🔥 Increase timeout (your logs show ~60s generation)
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", 120))


# =========================
# ⚡ STREAMING CONFIG
# =========================
# Enable/disable streaming (future toggle)
STREAM_ENABLED = os.getenv("STREAM_ENABLED", "true").lower() == "true"


# =========================
# ⚡ CACHE CONFIG (future use)
# =========================
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))


# =========================
# 🛠 DEBUG CONFIG
# =========================
DEBUG = os.getenv("DEBUG", "true").lower() == "true"