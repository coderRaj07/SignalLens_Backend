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
            You are analyzing changes between two versions of a competitor's website.

            Analyze ALL meaningful changes including:

            - Pricing updates
            - Feature additions or removals
            - Product changes
            - Policy changes
            - Messaging changes
            - Positioning changes
            - CTA or UX flow changes
            - Announcements
            - Structural or content updates

            Ignore:
            - Pure HTML formatting differences
            - Minor spacing changes
            - Tracking scripts
            - Metadata only updates

            Return your response strictly in this JSON format:

            {
            "significant": true or false,
            "change_types": ["pricing", "feature", "messaging", "structure", etc],
            "summary": "Clear business-focused summary in 3-6 bullet points.",
            "confidence": number from 0 to 100
            }

            If no meaningful change exists, return:

            {
            "significant": false,
            "change_types": [],
            "summary": "No meaningful business changes detected.",
            "confidence": 80
            }
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
