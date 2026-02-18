# import httpx
# from app.config import CEREBRAS_API_KEY
# from app.services.llm.base import BaseLLM

# CEREBRAS_ENDPOINT = "https://api.cerebras.ai/v1/chat/completions"

# class CerebrasProvider(BaseLLM):

#     async def chat(self, prompt: str) -> str:

#         headers = {
#             "Authorization": f"Bearer {CEREBRAS_API_KEY}",
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "model": "llama-3.1-8b-instruct",
#             "messages": [
#                 {"role": "system", "content": "You are a competitive intelligence analyst."},
#                 {"role": "user", "content": prompt}
#             ],
#             "temperature": 0.2
#         }

#         async with httpx.AsyncClient(timeout=30) as client:
#             response = await client.post(
#                 CEREBRAS_ENDPOINT,
#                 headers=headers,
#                 json=payload
#             )
#             response.raise_for_status()
#             data = response.json()
#             return data["choices"][0]["message"]["content"]
import httpx
from app.config import CEREBRAS_API_KEY
from app.services.llm.base import BaseLLM

CEREBRAS_ENDPOINT = "https://api.cerebras.ai/v1/chat/completions"

class CerebrasProvider(BaseLLM):

    async def chat(self, prompt: str) -> str:

        if not CEREBRAS_API_KEY:
            raise ValueError("CEREBRAS_API_KEY not configured")

        headers = {
            "Authorization": f"Bearer {CEREBRAS_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3.1-8b",   # ⚠ model name matters
            "messages": [
                {"role": "system", "content": "You are a competitive intelligence analyst."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                CEREBRAS_ENDPOINT,
                headers=headers,
                json=payload
            )

            response.raise_for_status()
            data = response.json()

            return data["choices"][0]["message"]["content"]
