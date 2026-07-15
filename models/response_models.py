from pydantic import BaseModel, Field


class FailureAnalysisResponse(BaseModel):

    summary: str = Field(
        description="Short summary of the failure"
    )

    rootCause: str = Field(
        description="Most likely root cause"
    )

    recommendation: str = Field(
        description="Recommended next action"
    )

    confidence: int = Field(
        ge=0,
        le=100,
        description="Confidence percentage"
    )