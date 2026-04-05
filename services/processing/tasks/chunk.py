from worker import celery
from db import get_conn

@celery.task
def chunk(segments, job_id):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE jobs SET progress=30 WHERE id=%s", (job_id,))
        conn.commit()

        chunks = []

        for i, seg in enumerate(segments):
            text = seg["text"].strip()
            if not text:
                continue

            chunks.append({
                "text": text,
                "start": seg["start"],
                "end": seg["end"],
                "index": i
            })

        return chunks

    finally:
        cur.close()
        conn.close()