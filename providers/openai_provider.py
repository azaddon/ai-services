import json

from openai import OpenAI

from providers.base_provider import BaseProvider
from services.config import Config
from utils.prompt_manager import PromptManager
from constants.prompt_names import PromptNames
from models.response_models import FailureAnalysisResponse

client = OpenAI(api_key=Config.OPENAI_KEY)


class OpenAIProvider(BaseProvider):

    def analyze(self, request):

        prompt = PromptManager.load_prompt(
            PromptNames.FAILURE_ANALYSIS
        )

        user_input = f"""
Test Name:
{request.testName}

Error:
{request.error}

Logs:
{request.logs}
"""

        try:

            response = client.chat.completions.create(

                model=Config.MODEL,

                temperature=0.2,

                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]

            )

            content = response.choices[0].message.content

            data = json.loads(content)

            return FailureAnalysisResponse(
                summary=data["summary"],
                rootCause=data["rootCause"],
                recommendation=data["recommendation"],
                confidence=data["confidence"]
            )

        except Exception as ex:

            print("OpenAI Error :", ex)

            return FailureAnalysisResponse(

                summary="AI analysis unavailable.",

                rootCause=str(ex),

                recommendation="Check AI service and OpenAI configuration.",

                confidence=0
            )