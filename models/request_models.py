from pydantic import BaseModel


class FailureAnalysisRequest(BaseModel):
    testName: str
    error: str
    logs: str