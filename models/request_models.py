from pydantic import BaseModel, ConfigDict, Field


class AutomationContext(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    testName: str | None = None

    browser: str | None = None

    environment: str | None = None

    url: str | None = None

    pageTitle: str | None = None

    stepName: str | None = None

    locator: str | None = None

    error: str | None = None

    stackTrace: str | None = None

    logs: list[str] = Field(default_factory=list, max_length=500)

    executionTime: int | None = None

    frameworkVersion: str

    playwrightVersion: str

    timestamp: str
    screenshotPath: str | None = None
    videoPath: str | None = None
    pageHtml: str | None = None

    screenshotBase64: str | None = None

class FailureAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    context: AutomationContext
