from services.config import Config

from providers.openai_provider import OpenAIProvider
from providers.ollama_provider import OllamaProvider


class ProviderFactory:

    @staticmethod
    def get_provider():

        if Config.LLM_PROVIDER.lower() == "openai":
            return OpenAIProvider()

        elif Config.LLM_PROVIDER.lower() == "ollama":
            return OllamaProvider()

        raise ValueError("Unsupported LLM Provider")