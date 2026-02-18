from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY
from app.services.llm.base import BaseLLM


class OpenAIProvider(BaseLLM):

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def chat(self, prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a competitive intelligence analyst."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"OpenAI LLM error: {str(e)}")
