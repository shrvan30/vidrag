#  Infrastructure & Deployment

##  Docker-Based Architecture

VidRAG is fully containerized using Docker Compose.
Each service runs in an isolated container and communicates over a shared Docker network.

---

##  Containers Overview

| Service        | Container Name          | Port | Description               |
| -------------- | ----------------------- | ---- | ------------------------- |
| PostgreSQL     | `vidrag_postgres`       | 5432 | Stores metadata & chunks  |
| Redis          | `vidrag_redis`          | 6379 | Celery broker + caching   |
| Ingestion      | `vidrag_ingestion`      | 8001 | Handles video ingestion   |
| Processing API | `vidrag_processing_api` | 8002 | ML pipeline trigger       |
| Worker         | `vidrag_worker`         | —    | Async processing (Celery) |
| Search         | `vidrag_search`         | 8003 | Hybrid retrieval          |
| Gateway        | `vidrag_gateway`        | 8000 | API entry point           |
| QA             | `vidrag_qa`             | 8004 | RAG-based QA              |

---

##  Container Commands

###  Ingestion Service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

* Accepts YouTube URL
* Extracts audio using `yt-dlp`

---

###  Processing API

```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

* Starts ML pipeline
* Triggers Celery tasks

---

###  Processing Worker

```bash
celery -A worker.celery worker --loglevel=info
```

* Executes async tasks:

  * Transcription
  * Chunking
  * Embedding

---

###  Search Service

```bash
uvicorn main:app --host 0.0.0.0 --port 8003
```

* Handles FAISS + BM25 retrieval
* Loads vector index into memory

---

###  Gateway

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

* Routes all API requests
* Acts as system entry point

---

###  QA Service

```bash
uvicorn main:app --host 0.0.0.0 --port 8004
```

* Implements RAG pipeline
* Calls LLM (`llama.cpp` endpoint)

---

##  Service Communication

Containers communicate using Docker DNS:

```text
http://search:8003
http://ingestion:8001
http://redis:6379
```

 No need for localhost inside containers

---

##  Volumes (Persistent Storage)

| Volume       | Purpose              |
| ------------ | -------------------- |
| `pgdata`     | PostgreSQL data      |
| `faiss_data` | Vector index storage |

 Ensures data persists across container restarts

---

##  Environment Variables

Defined in `.env`:

```
DATABASE_URL=postgresql://vidrag:vidrag@postgres:5432/vidrag
REDIS_URL=redis://redis:6379
HF_TOKEN=your_token
```

Used by:

* Ingestion
* Processing
* Search
* QA

---

##  Health Checks

Each service exposes:

* `/docs` (FastAPI Swagger)
* `/health` (optional)

### Example:

```bash
http://localhost:8001/docs
http://localhost:8003/docs
```

Used for:

* Service readiness
* Dependency management
* Preventing startup race conditions

---

##  Running the System

### Start all services

```bash
cd infra
docker-compose up --build
```

---

### Stop services

```bash
docker-compose down
```

---

### Rebuild containers

```bash
docker-compose up --build --force-recreate
```

---

##  Debugging & Logs

### View logs for a service

```bash
docker logs vidrag_search
docker logs vidrag_ingestion
```

---

### Enter container shell

```bash
docker exec -it vidrag_search bash
```

---

##  Key Infrastructure Strengths

###  Isolation

* Each service runs independently

###  Scalability

* Services can be scaled individually

###  Reliability

* Restart policies + health checks

###  Performance

* FAISS in-memory search
* Redis async processing

---
