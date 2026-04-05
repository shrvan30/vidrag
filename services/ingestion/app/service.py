import hashlib
from .db import get_conn
from sentence_transformers import SentenceTransformer

# ✅ Load model once (global)
model = SentenceTransformer("all-MiniLM-L6-v2")


# ==============================
# ✅ CREATE JOB
# ==============================
def create_job(url):
    conn = get_conn()
    cur = conn.cursor()

    url_hash = hashlib.sha256(url.encode()).hexdigest()

    # Insert video (avoid duplicates)
    cur.execute("""
        INSERT INTO videos (url_hash, source_url)
        VALUES (%s, %s)
        ON CONFLICT (url_hash) DO NOTHING
        RETURNING id;
    """, (url_hash, url))

    result = cur.fetchone()

    if result:
        video_id = result[0]
    else:
        cur.execute("SELECT id FROM videos WHERE url_hash=%s", (url_hash,))
        video_id = cur.fetchone()[0]

    # Create job
    cur.execute("""
        INSERT INTO jobs (video_id)
        VALUES (%s)
        RETURNING id;
    """, (video_id,))

    job_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return str(job_id), video_id


# ==============================
# ✅ INSERT CHUNKS (FIXED + SAFE)
# ==============================
def insert_chunks(video_id, transcript):
    if not transcript:
        print("⚠️ Empty transcript, skipping insert")
        return

    conn = get_conn()
    cur = conn.cursor()

    # ✅ Extract text safely
    texts = [t.get("text", "") for t in transcript]

    # ✅ Generate embeddings
    embeddings = model.encode(texts).tolist()

    data_to_insert = []

    for i, t in enumerate(transcript):
        text = t.get("text", "")
        start = float(t.get("start", 0))

        # 🔥 FIX: handle missing duration
        if i < len(transcript) - 1:
            next_start = float(transcript[i + 1].get("start", start + 2))
            end = next_start
        else:
            end = start + 2.0

        embedding = f"[{','.join(map(str, embeddings[i]))}]"

        data_to_insert.append((
            video_id,
            i,
            text,
            start,
            end,
            embedding
        ))

    # ✅ BULK INSERT (FASTER + CLEAN)
    cur.executemany("""
        INSERT INTO chunks (video_id, chunk_index, text, start_s, end_s, embedding)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (video_id, chunk_index) DO NOTHING;
    """, data_to_insert)

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Inserted {len(data_to_insert)} chunks successfully")