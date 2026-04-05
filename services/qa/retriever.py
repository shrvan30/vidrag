import httpx
import asyncio
from config import SEARCH_URL, TOP_K

# 🔥 Reuse client (important for performance)
client = httpx.AsyncClient(
    timeout=httpx.Timeout(10.0),
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
)

# 🔥 Retry config
MAX_RETRIES = 3
RETRY_DELAY = 0.5


async def retrieve(query: str, video_id: str):
    payload = {
        "query": query,
        "video_id": video_id,
        "top_k": TOP_K
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = await client.post(SEARCH_URL, json=payload)

            # 🔥 Raise for bad status
            response.raise_for_status()

            data = response.json()

            # 🔥 Validate response
            if "results" not in data:
                raise ValueError("Invalid response from search service")

            results = data["results"]

            # 🔥 Safety: ensure list
            if not isinstance(results, list):
                raise ValueError("Results is not a list")

            # 🔥 Limit top-k (extra safety)
            return results[:TOP_K]

        except (httpx.RequestError, httpx.HTTPStatusError, asyncio.TimeoutError) as e:
            print(f"[Retriever] Attempt {attempt+1} failed: {e}")

            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
            else:
                print("[Retriever] All retries failed")

        except Exception as e:
            print(f"[Retriever] Unexpected error: {e}")
            break

    # 🔥 Fallback (VERY IMPORTANT)
    return []