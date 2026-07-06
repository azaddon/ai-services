from services.config import Config

from providers.openai_provider import OpenAIProvider
from providers.ollama_provider import OllamaProvider


class ProviderFactory:

    @staticmethod
    def get_provider():

        provider = Config.LLM_PROVIDER.lower()

        if provider == "openai":
            return OpenAIProvider()

        elif provider == "ollama":
            return OllamaProvider()

        raise ValueError(f"Unsupported provider: {provider}")