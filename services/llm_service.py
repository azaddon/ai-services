from services.analysis_service import AnalysisService
from services.screenShot_service import ScreenshotService
from providers.openai_provider import OpenAIProvider

print("LOADED LLM SERVICE")
print(__file__)

class LLMService:

    @staticmethod
    def analyze(request):
        print("Inside analyze")
        print("===== LLMService.analyze() =====")

        rule_result = AnalysisService.rule_engine(request)

        print("Rule Engine Result:")
        print(rule_result)

        print("Calling ScreenshotService...")

        screenshot_result = ScreenshotService.analyze(request)

        print("Screenshot Result:")
        print(screenshot_result)

        return OpenAIProvider.analyze_with_openai(
            request,
            rule_result,
            screenshot_result
        )