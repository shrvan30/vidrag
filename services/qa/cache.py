import json
import hashlib
import asyncio
from typing import Optional

import redis.asyncio as redis

# 🔥 Global Redis client (async)
redis_client: Optional[redis.Redis] = None


# 🚀 Initialize connection (called in startup)
async def init_cache():
    global redis_client
    redis_client = redis.Redis(
        host="redis",
        port=6379,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True
    )


# 🔑 Key generator (namespaced)
def make_key(query: str, video_id: str) -> str:
    raw = f"{query}:{video_id}"
    return "qa_cache:" + hashlib.sha256(raw.encode()).hexdigest()


# 📥 Get cache
async def get_cache(key: str):
    if not redis_client:
        return None

    try:
        data = await redis_client.get(key)
        return json.loads(data) if data else None

    except Exception as e:
        print(f"[Cache] GET error: {e}")
        return None


# 📤 Set cache
async def set_cache(key: str, value, ttl: int = 3600):
    if not redis_client:
        return

    try:
        await redis_client.setex(key, ttl, json.dumps(value))

    except Exception as e:
        print(f"[Cache] SET error: {e}")


# ❌ Optional: delete cache
async def delete_cache(key: str):
    if redis_client:
        await redis_client.delete(key)


# 🧠 Optional: health check
async def cache_health():
    try:
        await redis_client.ping()
        return True
    except:
        return False