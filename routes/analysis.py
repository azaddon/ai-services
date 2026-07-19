from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.request_models import FailureAnalysisRequest
from models.response_models import FailureAnalysisResponse
from services.llm_service import LLMService

router = APIRouter()

@router.post("/api/v1/analysis/failures", response_model=FailureAnalysisResponse)
async def analyze(request: FailureAnalysisRequest):
    # request is a Pydantic model; .context exists
    result = LLMService.analyze(request)
    return JSONResponse(status_code=200, content=result)