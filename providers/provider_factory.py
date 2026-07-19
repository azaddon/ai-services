from providers.base_provider import BaseProvider
from services.config import Config
from providers.gemini_provider import GeminiProvider
from providers.openai_provider import OpenAIProvider
from providers.ollama_provider import OllamaProvider


class ProviderFactory:

    @staticmethod
    def get_provider()-> "BaseProvider":

        provider = Config.GEMINI_LLM_PROVIDER.lower()

        if provider == "openai":
            return OpenAIProvider()

        if provider == "ollama":
            return OllamaProvider()
        if provider == "gemini":
            return GeminiProvider()

        raise ValueError(f"Unsupported provider: {provider}")
