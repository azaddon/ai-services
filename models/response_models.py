from pydantic import BaseModel


class FailureAnalysisResponse(BaseModel):
    summary: str
    rootCause: str
    recommendation: str
    confidence: int