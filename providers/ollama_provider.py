from providers.base_provider import BaseProvider


class OllamaProvider(BaseProvider):

    def analyze(self, request, rule_result=None, screenshot_data_url=None):
        raise NotImplementedError("The Ollama provider is not implemented yet")
