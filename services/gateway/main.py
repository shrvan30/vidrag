from fastapi import FastAPI, Depends, WebSocket, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import httpx
import asyncio

from rate_limiter import rate_limiter
from config import INGESTION_URL, SEARCH_URL
from websocket import job_updates

app = FastAPI(title="VidRAG Gateway")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root
@app.get("/")
def root():
    return {"gateway": "running"}

# ✅ Health
@app.get("/health/all")
async def health():
    return {"gateway": "ok", "ingestion": "ok", "search": "ok"}

# 🔁 INGEST
@app.post("/ingest/url", dependencies=[Depends(rate_limiter)])
async def ingest(request: Request):
    data = await request.json()

    for attempt in range(5):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{INGESTION_URL}/ingest/url",
                    json=data
                )
            return response.json()

        except Exception:
            await asyncio.sleep(2)

    raise HTTPException(status_code=500, detail="Ingestion unavailable")

# 🔍 SEARCH
@app.post("/search", dependencies=[Depends(rate_limiter)])
async def search(request: Request):
    data = await request.json()

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{SEARCH_URL}/search",
                json=data
            )

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🤖 QA STREAM
@app.post("/qa", dependencies=[Depends(rate_limiter)])
async def qa(request: Request):
    data = await request.json()

    async def stream():
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    "http://qa:8004/qa",
                    json=data
                ) as response:

                    if response.status_code != 200:
                        yield "❌ QA service error".encode()
                        return

                    async for chunk in response.aiter_bytes():
                        if chunk:
                            yield chunk

        except Exception as e:
            print("❌ QA STREAM ERROR:", str(e))
            yield "❌ Gateway failed".encode()

    return StreamingResponse(stream(), media_type="text/plain")

# 🔌 WebSocket
@app.websocket("/ws/job/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await job_updates(websocket, job_id)