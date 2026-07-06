import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

    OPENAI_KEY = os.getenv("OPENAI_API_KEY")

    MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")