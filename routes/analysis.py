from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.request_models import FailureAnalysisRequest

from services.llm_service import LLMService

router = APIRouter()


@router.post("/analyze")
def analyze(request: FailureAnalysisRequest):

    try:
        return LLMService.analyze(request)
    except Exception as e:
        import traceback
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )