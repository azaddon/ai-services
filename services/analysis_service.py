from providers.openai_provider import OpenAIProvider


class AnalysisService:

    @staticmethod
    def analyze(request):
        root_cause = AnalysisService.rule_engine(request)

        if root_cause is None:
            return OpenAIProvider.analyze_with_openai(request)

        return root_cause

    @staticmethod
    def rule_engine(request):

        ctx = request.context

        error = (ctx.error or "").lower()

        if "locator" in error:
            return {
                "summary": "Element locator failed.",
                "rootCause": "Locator may have changed.",
                "recommendation": "Verify locator in Page Object.",
                "confidence": 95
            }

        if "timeout" in error:
            return {
                "summary": "Operation timed out.",
                "rootCause": "Element did not become ready.",
                "recommendation": "Review wait strategy.",
                "confidence": 92
            }

        if "assert" in error:
            return {
                "summary": "Assertion failed.",
                "rootCause": "Expected result does not match actual result.",
                "recommendation": "Review assertion or application behavior.",
                "confidence": 98
            }

        return None