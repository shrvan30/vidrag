from fastapi import FastAPI, HTTPException
from urllib.parse import urlparse, parse_qs

from .service import create_job, insert_chunks
from .transcript import fetch_transcript
from .db import get_conn

app = FastAPI()


def extract_video_id(url):
    return parse_qs(urlparse(url).query).get("v", [""])[0]


# ✅ NEW: get UUID using youtube_id
def get_or_create_video(conn, url, yt_id):
    cur = conn.cursor()

    # 🔍 Check if exists
    cur.execute(
        "SELECT id FROM videos WHERE url_hash = %s",
        (__import__("hashlib").sha256(url.encode()).hexdigest(),)
    )

    row = cur.fetchone()

    if row:
        return row[0]

    # 🆕 Create new
    cur.execute(
        """
        INSERT INTO videos (url_hash, source_url)
        VALUES (%s, %s)
        RETURNING id
        """,
        (__import__("hashlib").sha256(url.encode()).hexdigest(), url)
    )

    video_id = cur.fetchone()[0]
    conn.commit()

    return video_id


@app.get("/")
def root():
    return {"service": "ingestion running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest/url")
async def ingest_url(data: dict):
    try:
        url = data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL required")

        yt_id = extract_video_id(url)
        if not yt_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        conn = get_conn()

        # ✅ ALWAYS USE UUID
        video_id = get_or_create_video(conn, url, yt_id)

        print("🎬 Using video_id (UUID):", video_id)

        # ✅ Create job
        job_id, _ = create_job(url)

        # ✅ Fetch transcript
        transcript = fetch_transcript(yt_id)
        print(f"📜 {len(transcript)} segments")

        # ✅ Insert chunks with UUID
        insert_chunks(video_id, transcript)

        return {
            "status": "completed",
            "video_id": str(video_id),
            "chunks": len(transcript)
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        return {
            "status": "error",
            "error": str(e)
        }