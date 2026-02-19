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

        system_prompt = """
            You are analyzing a competitor website update.

            Focus ONLY on:
            - Pricing changes
            - Feature additions or removals
            - Policy updates
            - Product updates

            Ignore:
            - Layout changes
            - HTML tags
            - Metadata

            If no meaningful business change exists, reply exactly:
            "No significant business changes detected."
            """

        payload = {
            "model": "llama3.1-8b",   # Make sure this model exists in Cerebras
            "messages": [
                {"role": "system", "content": system_prompt},
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
