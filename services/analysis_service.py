class AnalysisService:
    @staticmethod
    def rule_engine(request):
        # get context in a safe way
        if hasattr(request, "context"):
            ctx = request.context
        elif isinstance(request, dict):
            ctx = request.get("context")
        else:
            ctx = None

        # existing logic that used ctx
        # example placeholder:
        if not ctx:
            return {}

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
