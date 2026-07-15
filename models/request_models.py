from pydantic import BaseModel
from typing import Optional


class AutomationContext(BaseModel):

    testName: str | None = None

    browser: str | None = None

    environment: str | None = None

    url: str | None = None

    pageTitle: str | None = None

    stepName: str | None = None

    locator: str | None = None

    error: str | None = None

    stackTrace: str | None = None

    logs: list[str] = []

    executionTime: int | None = None

    frameworkVersion: str

    playwrightVersion: str

    timestamp: str
    screenshotPath: Optional[str] = None
    videoPath: Optional[str] = None
    pageHtml: str | None = None

    screenshotBase64: str | None = None

class FailureAnalysisRequest(BaseModel):

    context: AutomationContext