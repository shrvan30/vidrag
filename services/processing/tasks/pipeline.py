from celery import chain
from tasks.transcribe import transcribe
from tasks.chunk import chunk
from tasks.embed import embed
from tasks.store import store_chunks
import redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def publish(job_id, message):
    r.publish(job_id, message)

def process_pipeline(job_id, audio_path):
    return chain(
        transcribe.s(job_id, audio_path),
        chunk.s(job_id),
        embed.s(job_id),
        store_chunks.s(job_id)
    ).apply_async()