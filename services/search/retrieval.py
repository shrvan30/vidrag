import numpy as np
import faiss

from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi

from config import TOP_K, FINAL_K, FAISS_WEIGHT, BM25_WEIGHT

# ✅ Load models once
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


# 🔥 BATCH EMBEDDING (CRITICAL FOR LONG VIDEOS)
def batch_encode(texts, batch_size=64):
    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        emb = embed_model.encode(
            batch,
            show_progress_bar=False
        )

        embeddings.append(emb)

    return np.vstack(embeddings)


def normalize(scores):
    if len(scores) == 0:
        return []

    min_s = float(min(scores))
    max_s = float(max(scores))

    if max_s - min_s == 0:
        return [0.0] * len(scores)

    return [(float(s) - min_s) / (max_s - min_s) for s in scores]


class VideoIndex:
    def __init__(self, chunks):
        if not chunks or len(chunks) == 0:
            raise ValueError("❌ No chunks provided")

        # 🔥 LIMIT FOR STABILITY (important for 3hr videos)
        MAX_CHUNKS = 3000
        chunks = chunks[:MAX_CHUNKS]

        self.chunks = chunks

        texts = [c.get("text", "") for c in chunks if c.get("text")]

        if len(texts) == 0:
            raise ValueError("❌ All chunks are empty")

        print(f"⚡ Generating embeddings for {len(texts)} chunks...")

        # ✅ Batch embedding
        self.embeddings = batch_encode(texts)

        # ✅ Convert to float32 (FAISS requirement)
        self.embeddings = np.array(self.embeddings).astype("float32")

        # 🔥 Safety checks
        if len(self.embeddings.shape) != 2:
            raise ValueError("❌ Invalid embeddings shape")

        if len(self.embeddings) == 0:
            raise ValueError("❌ No embeddings generated")

        dim = self.embeddings.shape[1]

        print(f"📐 Embedding shape: {self.embeddings.shape}")

        # ✅ FAISS
        self.faiss = faiss.IndexFlatIP(dim)
        self.faiss.add(self.embeddings)

        # ✅ BM25
        tokenized = [t.split() for t in texts]
        self.bm25 = BM25Okapi(tokenized)


def hybrid_search(query, video_index):
    if not video_index or not video_index.chunks:
        return []

    try:
        query_emb = embed_model.encode([query])[0]

        D, I = video_index.faiss.search(
            np.array([query_emb]).astype("float32"),
            k=min(TOP_K, len(video_index.chunks))
        )

        faiss_scores = normalize(D[0])
        faiss_indices = I[0]

        faiss_dict = {
            idx: faiss_scores[i]
            for i, idx in enumerate(faiss_indices)
            if idx >= 0
        }

        bm25_scores = video_index.bm25.get_scores(query.split())
        bm25_scores = normalize(bm25_scores)

        results = []

        for i, chunk in enumerate(video_index.chunks):
            faiss_score = faiss_dict.get(i, 0.0)
            bm25_score = bm25_scores[i] if i < len(bm25_scores) else 0.0

            score = (
                FAISS_WEIGHT * faiss_score +
                BM25_WEIGHT * bm25_score
            )

            if score > 0:
                results.append({
                    "index": i,
                    "text": chunk.get("text", ""),
                    "start_s": chunk.get("start_s", 0),
                    "end_s": chunk.get("end_s", 0),
                    "score": float(score)
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:FINAL_K]

    except Exception as e:
        print("❌ Hybrid search error:", e)
        return []


def add_context(results, chunks, window=1):
    final = []

    for r in results:
        idx = r.get("index")

        if idx is None or idx >= len(chunks):
            continue

        start = max(0, idx - window)
        end = min(len(chunks) - 1, idx + window)

        context = " ".join(
            chunks[i].get("text", "") for i in range(start, end + 1)
        )

        r["context"] = context
        final.append(r)

    return final


def rerank(query, results):
    if not results:
        return results

    try:
        pairs = [(query, r.get("text", "")) for r in results]
        scores = reranker.predict(pairs)

        for i, s in enumerate(scores):
            results[i]["score"] = float(s)

        results.sort(key=lambda x: x["score"], reverse=True)

    except Exception as e:
        print("⚠️ Rerank failed:", e)

    return results