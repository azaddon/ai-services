from providers.provider_factory import ProviderFactory


class LLMService:

    @staticmethod
    def analyze(request):

        provider = ProviderFactory.get_provider()

        return provider.analyze(request)