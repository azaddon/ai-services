from services.analysis_service import AnalysisService
from services.screenShot_service import ScreenshotService
from providers.provider_factory import ProviderFactory
from services.history_service import HistoryService
import logging 

logger = logging.getLogger(__name__)

class LLMService:
    @staticmethod
    def _get_context(request):
        if hasattr(request, "context"):
            return request.context
        if isinstance(request, dict):
            return request.get("context")
        return None

    @staticmethod
    def analyze(request):
        # request may be Pydantic model or dict
        rule_result = AnalysisService.rule_engine(request)
        screenshot_data_url = ScreenshotService.get_data_url(LLMService._get_context(request))
        try:
            raw_result = ProviderFactory.get_provider().analyze(
                request, rule_result, screenshot_data_url
            )
        except Exception as e:
            # Log and return a safe error object instead of letting the request 500
            #logger = __import__("logging").getLogger(__name__)
            logger.exception("AI provider failed: %s", e)
            raw_result = {
                "status": "error",
                "message": "AI analysis unavailable",
                "detail": str(e)
            }
        try:
            HistoryService.save(request, raw_result)
        except Exception:
            logger.exception("Failed to save history")
        return raw_result
