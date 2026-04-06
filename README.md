# VidRAG – Video Retrieval-Augmented Generation System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-green)
![Architecture](https://img.shields.io/badge/Microservices-Distributed-orange)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

---

## What is VidRAG?

VidRAG is a **distributed AI system** that allows users to:

*  Ingest YouTube videos
*  Convert speech → text (Whisper)
*  Search content semantically + via keywords
*  Ask questions using RAG (LLM)
*  Jump to exact timestamps in video

 It transforms **unstructured video into searchable knowledge**

---

##  Why This Project Matters

Most video platforms (YouTube, courses, lectures):

 Not searchable semantically
 No deep understanding of content
 Hard to extract knowledge

 VidRAG solves this using:

* Retrieval-Augmented Generation (RAG)
* Hybrid search (FAISS + BM25)
* LLM-based reasoning

---

##  Key Innovation

###  Hybrid Retrieval

* FAISS → semantic understanding
* BM25 → keyword precision
* CrossEncoder → context ranking

###  CPU-Based LLM Inference

Uses **`llama.cpp`** for:

* Running LLMs locally
* No GPU dependency
* Cost-efficient deployment

👉 This makes the system **accessible + scalable**

---

##  System Overview

```text
User → Gateway → Ingestion → Processing → Search → QA → Frontend
```

 Detailed docs:

* Architecture → `docs/ARCHITECTURE.md`
* Services → `docs/services.md`
* Frontend → `docs/frontend.md`
* Infrastructure → `docs/infra.md`

---

##  Tech Stack

* **Backend:** FastAPI, PostgreSQL, Redis
* **ML:** Whisper, SentenceTransformers, CrossEncoder
* **Search:** FAISS + BM25
* **LLM:** llama.cpp / Phi-3
* **Frontend:** React + Vite
* **Infra:** Docker

---

##  Demo

###  Demo 1 — Video Q&A using RAG

![Demo 1](docs/images/demo_1.png)

This demo shows how VidRAG enables **question answering directly from video content**.

* User inputs a query related to the video
* System retrieves relevant transcript chunks
* LLM generates context-aware answer
* Response is grounded in video content

---

###  Demo 2 — Semantic Search & Firebase Key Detection

![Demo 2](docs/images/demo_2.png)

This demo highlights **hybrid semantic search with timestamp navigation**.

* FAISS + BM25 retrieves relevant segments
* Detects technical keywords like *Firebase*, *private key*
* Displays exact timestamps for quick navigation
* Generates quick insights from retrieved context

---


##  Quick Start

```bash
cd infra
docker-compose up --build
```

---

##  Use Cases

*  Lecture understanding
*  Video content search
*  Knowledge extraction
*  AI-powered learning

---

##  Author

Shravan Upadhye
