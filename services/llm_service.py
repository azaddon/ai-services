from models.request_models import FailureAnalysisRequest
from models.response_models import FailureAnalysisResponse


class LLMService:

    @staticmethod
    def analyze(request: FailureAnalysisRequest):

        return FailureAnalysisResponse(

            summary="Login test failed.",

            rootCause="Unable to determine yet.",

            recommendation="Investigate Playwright logs.",

            confidence=50

        )