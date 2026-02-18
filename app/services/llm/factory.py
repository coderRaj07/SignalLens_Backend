from app.config import LLM_PROVIDER
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.cerebras_provider import CerebrasProvider


def get_llm_provider():
    provider = LLM_PROVIDER.lower()

    if provider == "openai":
        return OpenAIProvider()

    if provider == "cerebras":
        return CerebrasProvider()

    raise ValueError("Invalid LLM_PROVIDER configured")
