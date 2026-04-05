import httpx
import json
from config import LLM_URL


async def stream_answer(prompt: str):
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            LLM_URL,
            json={
                "prompt": prompt,
                "n_predict": 256,          # 🔥 upgraded
                "temperature": 0.15,       # 🔥 more accurate
                "top_p": 0.9,
                "repeat_penalty": 1.15,
                "stream": True,
            },
        ) as response:

            buffer = ""

            async for chunk in response.aiter_text():
                if not chunk:
                    continue

                buffer += chunk

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()

                    if not line:
                        continue

                    if line.startswith("data:"):
                        line = line.replace("data:", "").strip()

                    try:
                        data = json.loads(line)

                        token = data.get("content")

                        if token:
                            yield token

                        if data.get("stop"):
                            return

                    except:
                        continue