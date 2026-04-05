import whisper
from worker import celery
from db import get_conn

model = None


# =========================
# 🔥 LOAD MODEL (ONCE)
# =========================
def get_model():
    global model
    if model is None:
        print("🔥 Loading Whisper model...")
        model = whisper.load_model("base")  # use "small" if GPU available
    return model


# =========================
# 🔥 TRANSCRIBE TASK
# =========================
@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3}
)
def transcribe(self, job_id, audio_path):
    conn = get_conn()
    cur = conn.cursor()

    try:
        # 🔄 Step 1: progress
        cur.execute(
            "UPDATE jobs SET status='processing', progress=10 WHERE id=%s",
            (job_id,)
        )
        conn.commit()

        # 🔥 Load model
        model = get_model()

        # 🔥 Transcribe
        result = model.transcribe(audio_path)

        segments = result.get("segments", [])

        if not segments:
            raise Exception("No speech detected")

        # 🔄 Step 2: progress
        cur.execute(
            "UPDATE jobs SET progress=70 WHERE id=%s",
            (job_id,)
        )
        conn.commit()

        # =========================
        # ✅ FORMAT FOR YOUR PIPELINE
        # =========================
        formatted = []

        for seg in segments:
            formatted.append({
                "text": seg.get("text", "").strip(),
                "start": float(seg.get("start", 0)),
                "end": float(seg.get("end", 0))
            })

        # 🔄 Step 3: done
        cur.execute(
            "UPDATE jobs SET status='completed', progress=100 WHERE id=%s",
            (job_id,)
        )
        conn.commit()

        print(f"✅ Transcription complete: {len(formatted)} segments")

        return formatted

    except Exception as e:
        conn.rollback()

        # ❌ mark failed
        cur.execute(
            """
            UPDATE jobs 
            SET status='failed', error=%s 
            WHERE id=%s
            """,
            (str(e), job_id)
        )
        conn.commit()

        print("❌ Transcription failed:", str(e))
        raise

    finally:
        cur.close()
        conn.close()