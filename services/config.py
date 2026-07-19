import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    OPENAI_LLM_PROVIDER = os.getenv("OPENAI_LLM_PROVIDER", "openai")

    OPENAI_KEY = os.getenv("OPENAI_API_KEY")

    MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    GEMINI_LLM_PROVIDER = os.getenv("GEMINI_LLM_PROVIDER", "gemini")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    MODEL_FALLBACKS = os.getenv("MODEL_FALLBACKS", "gemini-3.5-flash,gemini-3.1-flash-lite").split(",")
    AI_TIMEOUT_MS = int(os.getenv("AI_TIMEOUT_MS", "60000"))   # 60 seconds default
    # or use seconds:
    AI_TIMEOUT_S = int(os.getenv("AI_TIMEOUT_S", "60"))
    AI_RETRIES = int(os.getenv("AI_RETRIES", "2"))
    REQUEST_TIMEOUT_SECONDS = float(os.getenv("LLM_REQUEST_TIMEOUT_SECONDS", "45"))

    MAX_SCREENSHOT_BYTES = int(os.getenv("MAX_SCREENSHOT_BYTES", str(8 * 1024 * 1024)))

    ALLOW_LOCAL_SCREENSHOT_PATHS = os.getenv(
        "ALLOW_LOCAL_SCREENSHOT_PATHS", "false"
    ).lower() in {"1", "true", "yes"}

    MONGO_URI = os.getenv("MONGO_URI")

    MONGO_DATABASE = os.getenv("MONGO_DATABASE", "ai_test_assistant")

    MONGO_CONNECT_TIMEOUT_MS = int(os.getenv("MONGO_CONNECT_TIMEOUT_MS", "3000"))
