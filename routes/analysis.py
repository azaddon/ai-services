from fastapi import APIRouter

from models.request_models import FailureAnalysisRequest

from services.llm_service import LLMService

router = APIRouter()


@router.post("/analyze")
def analyze(request: FailureAnalysisRequest):

    return LLMService.analyze(request)