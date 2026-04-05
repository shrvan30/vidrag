from fastapi import WebSocket
import redis.asyncio as redis
from config import REDIS_URL

async def job_updates(websocket: WebSocket, job_id: str):
    await websocket.accept()

    r = redis.from_url(REDIS_URL, decode_responses=True)
    pubsub = r.pubsub()

    await pubsub.subscribe(job_id)

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)

            if message:
                await websocket.send_text(message["data"])
    except:
        await pubsub.unsubscribe(job_id)
        await websocket.close()