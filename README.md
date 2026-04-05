# 🎬 VidRAG – Video Retrieval-Augmented Generation System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-green)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-orange)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

---

## 🚀 Overview

**VidRAG** is a distributed, microservices-based AI system that enables:

- 🎥 YouTube video ingestion
- 🧠 Speech-to-text transcription (Whisper)
- 🔍 Hybrid semantic + keyword search
- 🤖 Retrieval-Augmented Generation (RAG)
- ⏱️ Timestamp-based video navigation

It combines **ML + Systems Design + Full-stack engineering** into a production-ready application.

---

## ✨ Key Features

- 🔎 **Hybrid Retrieval**
  - FAISS (semantic search)
  - BM25 (keyword matching)
  - Cross-Encoder reranking

- 🤖 **RAG Pipeline**
  - Context-aware answer generation
  - Timestamp-linked responses

- ⚡ **Microservices Architecture**
  - Independent, scalable services
  - Fault isolation

- 🐳 **Dockerized Infrastructure**
  - Fully containerized system
  - One-command deployment

- 🎥 **Interactive UI**
  - Video playback
  - Click-to-seek timestamps
  - Chat-based QA

---

## 🧠 System Architecture

# 🎬 VidRAG – System Architecture

## 📌 Overview

VidRAG is a **distributed, microservices-based Retrieval-Augmented Generation (RAG) system** designed to enable semantic understanding and querying of video content.

It allows users to:

* Ingest YouTube videos
* Transcribe and process audio
* Perform hybrid search (semantic + keyword)
* Ask natural language questions
* Navigate videos using timestamped results

The system combines **machine learning, information retrieval, and scalable backend engineering** into a production-ready pipeline.

---

## 🧠 High-Level Architecture

### 🔁 Data Flow

User → Gateway → Ingestion → Processing → Search → QA → Frontend

### 🔄 Pipeline Breakdown

1. **User submits YouTube URL**
2. Ingestion service extracts audio
3. Processing service:

   * Transcribes audio (Whisper)
   * Chunks text
   * Generates embeddings
4. Search service:

   * Performs hybrid retrieval (FAISS + BM25)
5. QA service:

   * Uses retrieved chunks for RAG
6. Frontend:

   * Displays answers + timestamps
   * Syncs video playback

---

## 🧩 Microservices Architecture

VidRAG consists of independently deployable services:

| Service        | Port | Responsibility                     |
| -------------- | ---- | ---------------------------------- |
| Gateway        | 8000 | API routing & orchestration        |
| Ingestion      | 8001 | Video ingestion & audio extraction |
| Processing API | 8002 | ML pipeline trigger                |
| Worker         | —    | Async task execution (Celery)      |
| Search         | 8003 | Hybrid retrieval                   |
| QA             | 8004 | RAG-based question answering       |
| PostgreSQL     | 5432 | Metadata & chunk storage           |
| Redis          | 6379 | Task queue + caching               |

---

## 1️⃣ API Gateway

**Role:**

* Central entry point
* Routes requests to services
* Abstracts internal architecture

**Key Features:**

* Request forwarding
* WebSocket support (real-time updates)
* Rate limiting (extensible)

---

## 2️⃣ Ingestion Service

**Role:**

* Accepts YouTube URLs
* Downloads audio using `yt-dlp`
* Stores metadata

**Pipeline:**

YouTube URL → Audio Extraction → Store in `/data`

**Storage:**

* PostgreSQL (video metadata)
* Local volume (`/data`)

---

## 3️⃣ Processing Service

### Components:

* FastAPI (trigger API)
* Celery Worker (async execution)
* Redis (broker)

### Pipeline:

Audio
↓
Whisper Transcription
↓
Chunking (300 tokens + overlap)
↓
Embedding (SentenceTransformers MiniLM)
↓
Storage + Indexing

---

## 4️⃣ Search Service

**Role:**
Implements hybrid retrieval strategy

### Retrieval Pipeline:

1. FAISS → semantic similarity
2. BM25 → keyword matching
3. Score fusion
4. CrossEncoder reranking

### Scoring Formula:

Final Score = (0.65 × FAISS) + (0.35 × BM25)

---

## 5️⃣ QA Service (RAG Engine)

**Flow:**

User Query
↓
Search Service (Top-K chunks)
↓
Prompt Construction
↓
LLM (llama.cpp / Phi-3)
↓
Answer Generation

**Output:**

```json
{
  "answer": "...",
  "sources": [120, 340],
  "confidence": 0.78
}
```

---

## 🗄️ Data Layer

### PostgreSQL (pgvector)

Stores:

* Video metadata
* Text chunks
* Embeddings (optional)

### Redis

* Celery message broker
* Caching layer
* Pub/Sub support

### FAISS

* Disk-based vector index
* Loaded into memory for fast retrieval

---

## 🌐 Frontend Architecture

### Tech Stack:

* React + Vite
* TailwindCSS

### Components:

| Component   | Role                 |
| ----------- | -------------------- |
| UrlInput    | Accepts YouTube link |
| VideoPlayer | Displays video       |
| SearchBar   | Query input          |
| ResultsList | Shows search results |
| ChatBox     | RAG-based QA         |

---

## 🎥 Video Playback Design

* Uses YouTube iframe embed
* Timestamp navigation via `?start=seconds`
* Avoids ReactPlayer for reliability

---

## 🔍 Retrieval System Design

### Hybrid Approach

| Method       | Purpose                |
| ------------ | ---------------------- |
| FAISS        | Semantic understanding |
| BM25         | Keyword precision      |
| CrossEncoder | Context-aware ranking  |

### Why Hybrid?

* FAISS → captures meaning
* BM25 → captures exact matches
* Combined → higher accuracy

---

## ⚙️ Infrastructure & DevOps

### Dockerized Services

* Each service runs in its own container
* Communicate via internal Docker network

### Example Internal URLs:

http://search:8003
http://ingestion:8001

---

### Volumes

```yaml
pgdata:
faiss_data:
```

* Ensures persistence across restarts

---

### Environment Variables

Stored in `.env`

```
DATABASE_URL=
REDIS_URL=
HF_TOKEN=
```

---

### Health Checks

Each service exposes `/health` or `/docs`

Used for:

* Dependency management
* Startup ordering
* Reliability

---

## 🚀 System Strengths

### ✅ Scalability

* Independent services
* Easy horizontal scaling

### ✅ Fault Isolation

* Failure in one service doesn’t crash others

### ✅ Performance

* FAISS enables fast vector search
* Redis enables async processing

### ✅ Real-Time UX

* Timestamp navigation
* Fast query responses

---

## ⚠️ Challenges & Solutions

| Problem               | Solution                  |
| --------------------- | ------------------------- |
| FAISS crashes         | Safe loading + validation |
| Docker issues         | Clean rebuild strategy    |
| Video playback issues | Switched to iframe        |
| Async failures        | Celery + retry logic      |

---

## 🔮 Future Improvements

* Multi-video search
* Auto chapter generation
* OCR on video frames
* Analytics dashboard
* Cloud deployment (AWS/GCP)

---

## 🏁 Conclusion

VidRAG demonstrates:

* Distributed systems design
* Machine learning pipeline integration
* Retrieval-Augmented Generation (RAG)
* Full-stack development
* Production-ready engineering practices

---

## 👨‍💻 Author

Shravan Upadhye
PICT Pune
### 🔁 Flow

User → Gateway → Ingestion → Processing → Search → QA → UI


---

## ⚙️ Tech Stack

### 🔹 Backend
- FastAPI
- PostgreSQL (pgvector)
- Redis (Celery broker + caching)
- FAISS (vector search)

### 🔹 Machine Learning
- Whisper (speech-to-text)
- SentenceTransformers (embeddings)
- CrossEncoder (reranking)
- LLM (llama.cpp / Phi-3)

### 🔹 Frontend
- React + Vite
- TailwindCSS

### 🔹 DevOps
- Docker & Docker Compose
- Microservices architecture

---

## 🐳 Setup Instructions

--cd infra
--docker-compose up --build
