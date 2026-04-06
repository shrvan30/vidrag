#  Backend Services

## Gateway

* Routes all requests
* Handles orchestration

## Ingestion

* Downloads audio via yt-dlp
* Stores metadata

## Processing

* Whisper transcription
* Chunking + embeddings
* Celery async pipeline

## Search

* FAISS (semantic)
* BM25 (keyword)
* Hybrid scoring

## QA

* RAG pipeline
* LLM inference (llama.cpp)

---

## Retrieval Formula

Final Score = 0.65 × FAISS + 0.35 × BM25
