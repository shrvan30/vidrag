from fastapi import FastAPI, HTTPException

from db import load_chunks
from cache import get_video_index
from retrieval import hybrid_search, add_context, rerank

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search")
def search_api(data: dict):
    try:
        query = data.get("query")
        video_id = data.get("video_id")

        if not query:
            raise HTTPException(status_code=400, detail="Query is required")

        if not video_id:
            raise HTTPException(status_code=400, detail="video_id is required")

        print(f"🔍 Query: {query}")
        print(f"🎬 Video ID: {video_id}")

        # ✅ Load chunks first
        chunks = load_chunks(video_id)

        if not chunks:
            print(f"❌ No chunks found for video_id: {video_id}")
            return {
                "error": "No data found. Try reprocessing video.",
                "results": []
            }

        print(f"✅ Loaded {len(chunks)} chunks")

        # ✅ Cache-safe loading
        video_index = get_video_index(video_id, lambda vid: chunks)

        if not video_index:
            return {"results": []}

        # ✅ Pipeline
        results = hybrid_search(query, video_index)
        results = add_context(results, video_index.chunks)
        results = rerank(query, results)

        formatted = [
            {
                "text": r.get("text", ""),
                "start": r.get("start_s", 0),
                "end": r.get("end_s", r.get("start_s", 0) + 5),
                "score": float(r.get("score", 0))
            }
            for r in results
        ]

        return {"results": formatted}

    except Exception as e:
        import traceback
        print("❌ SEARCH ERROR:")
        traceback.print_exc()

        return {
            "error": str(e),
            "results": []
        }