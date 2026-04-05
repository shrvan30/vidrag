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

📄 Detailed Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

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

cd infra
docker-compose up --build