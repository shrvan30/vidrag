from sentence_transformers import SentenceTransformer
from worker import celery
from db import get_conn

embed_model = None

def get_embed_model():
    global embed_model
    if embed_model is None:
        print("Loading embedding model...")
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    return embed_model

@celery.task
def embed(chunks, job_id):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE jobs SET progress=60 WHERE id=%s", (job_id,))
        conn.commit()

        model = get_embed_model()
        texts = [c["text"] for c in chunks]

        embeddings = model.encode(texts, show_progress_bar=False)

        for i, emb in enumerate(embeddings):
            chunks[i]["embedding"] = emb.tolist()

        return chunks

    finally:
        cur.close()
        conn.close()