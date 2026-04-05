from worker import celery
from db import get_conn

@celery.task(bind=True)
def store_chunks(self, chunks, job_id):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE jobs SET progress=90 WHERE id=%s", (job_id,))
        conn.commit()

        cur.execute("SELECT video_id FROM jobs WHERE id=%s", (job_id,))
        video_id = cur.fetchone()[0]

        for c in chunks:
            cur.execute("""
                INSERT INTO chunks 
                (video_id, chunk_index, text, start_s, end_s, embedding)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                video_id,
                c["index"],
                c["text"],
                c["start"],
                c["end"],
                c["embedding"]
            ))

        cur.execute("""
            UPDATE jobs SET status='completed', progress=100
            WHERE id=%s
        """, (job_id,))

        conn.commit()

    except Exception as e:
        conn.rollback()

        # ❌ mark failed
        cur.execute("""
            UPDATE jobs SET status='failed'
            WHERE id=%s
        """, (job_id,))
        conn.commit()

        raise e

    finally:
        cur.close()
        conn.close()