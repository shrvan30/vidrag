from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from retriever import retrieve
from prompt import build_prompt
from llm_client import stream_answer
from utils import select_diverse_chunks
from config import CONTEXT_LIMIT

app = FastAPI()


# =========================
# 🔹 Request Schema
# =========================
class QARequest(BaseModel):
    question: str
    video_id: str


# =========================
# 🔹 Health Check
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# 🔥 STREAMING QA ENDPOINT
# =========================
@app.post("/qa")
async def qa_stream(request: QARequest):

    question = request.question.strip()
    video_id = request.video_id

    if not question:
        raise HTTPException(status_code=400, detail="Empty question")

    print(f"🧠 QA Question: {question}")
    print(f"🎬 Video ID: {video_id}")

    # =========================
    # 🔍 Retrieve relevant chunks
    # =========================
    chunks = await retrieve(question, video_id)

    if not chunks:
        raise HTTPException(status_code=404, detail="No relevant context found")

    print(f"📦 Retrieved {len(chunks)} chunks")

    # =========================
    # 🎯 Select diverse + filter low quality
    # =========================
    selected = select_diverse_chunks(chunks, CONTEXT_LIMIT)

    # 🔥 Remove low-score chunks (improves answer quality)
    selected = [c for c in selected if c.get("score", 0) > 0.2]

    if not selected:
        raise HTTPException(status_code=404, detail="No high-quality context found")

    print(f"✅ Selected {len(selected)} high-quality chunks")

    # =========================
    # 🧠 Build rich context
    # =========================
    context = "\n\n".join([
        c.get("context", c.get("text", ""))
        for c in selected
    ])

    # 🔥 Debug what LLM sees
    print("\n===== QA CONTEXT PREVIEW =====")
    print(context[:1000])  # preview only
    print("================================\n")

    # =========================
    # 🧾 Build prompt (IMPORTANT)
    # =========================
    prompt = build_prompt(question, selected)

    # =========================
    # ⚡ Streaming generator
    # =========================
    async def token_generator():
        try:
            async for token in stream_answer(prompt):
                yield token.encode("utf-8")

        except Exception as e:
            print(f"[STREAM ERROR] {e}", flush=True)
            yield b"\n[Error generating response]"

    # =========================
    # 📡 Return streaming response
    # =========================
    return StreamingResponse(
        token_generator(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Transfer-Encoding": "chunked",
        },
    )