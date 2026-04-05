import redis.asyncio as redis
from fastapi import Request, HTTPException

r = redis.from_url("redis://redis:6379", decode_responses=True)

RATE_LIMIT = 60  # requests
WINDOW = 60      # seconds


async def rate_limiter(request: Request):
    ip = request.client.host
    key = f"rate_limit:{ip}"

    count = await r.incr(key)

    if count == 1:
        await r.expire(key, WINDOW)

    if count > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")