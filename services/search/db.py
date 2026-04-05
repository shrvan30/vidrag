import os
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL not set")

    url = urlparse(DATABASE_URL)

    return psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )


# 🔥 ADD THIS FUNCTION (MISSING PART)
def load_chunks(video_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT chunk_index, text, start_s, end_s, embedding
        FROM chunks
        WHERE video_id = %s
        ORDER BY chunk_index
    """, (video_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    # Convert to usable format
    chunks = []
    for r in rows:
        chunks.append({
            "chunk_index": r[0],
            "text": r[1],
            "start_s": r[2],
            "end_s": r[3],
            "embedding": r[4]
        })

    print(f"✅ Loaded {len(chunks)} chunks from DB")

    return chunks