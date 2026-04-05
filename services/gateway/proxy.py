import httpx
import asyncio

async def forward_request(url, data):
    for attempt in range(5):   # retry 5 times
        try:
            print(f"📤 Forwarding request to {url} | Attempt {attempt+1}")

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, json=data)

                print(f"✅ Success from {url}")
                return response.json()

        except Exception as e:
            print(f"❌ Attempt {attempt+1} failed:", e)
            await asyncio.sleep(2)

    raise Exception(f"🚨 Service unavailable: {url}")