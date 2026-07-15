from openai import OpenAI

from providers.base_provider import BaseProvider
from services.config import Config
from utils.prompt_manager import PromptManager
from constants.prompt_names import PromptNames
from models.response_models import FailureAnalysisResponse

client = OpenAI(api_key=Config.OPENAI_KEY)


class OpenAIProvider(BaseProvider):

    def analyze_with_openai(request, rule_result, screenshot_result):

        # -------------------------
        # STEP 5 STARTS HERE
        # -------------------------

        prompt = PromptManager.get_prompt(
            PromptNames.FAILURE_ANALYSIS
        )

        ctx = request.context

        user_input = f"""
Rule Engine Analysis:

{rule_result}

Screenshot Analysis:

{screenshot_result}

Test Name:
{ctx.testName}

Browser:
{ctx.browser}

Environment:
{ctx.environment}

URL:
{ctx.url}

Page Title:
{ctx.pageTitle}

Step:
{ctx.stepName}

Locator:
{ctx.locator}

Execution Time:
{ctx.executionTime}

Error:
{ctx.error}

Stack Trace:
{ctx.stackTrace}

Screenshot Analysis:
{screenshot_result}

Logs:
{ctx.logs}
"""

        # -------------------------
        # STEP 5 ENDS HERE
        # -------------------------

        # -------------------------
        # STEP 6 STARTS HERE
        # -------------------------

        completion = client.beta.chat.completions.parse(

            model=Config.MODEL,

            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],

            response_format=FailureAnalysisResponse
        )

        return completion.choices[0].message.parsed

        # -------------------------
        # STEP 6 ENDS HERE
        # -------------------------