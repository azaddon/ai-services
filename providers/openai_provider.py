# from pathlib import Path
# from openai import OpenAI

# from services.config import Config
# from models.request_models import FailureAnalysisRequest

# client = OpenAI(api_key=Config.OPENAI_KEY)

# PROMPT = Path(
#     "prompts/failure_prompt.txt"
# ).read_text(encoding="utf-8")


# class OpenAIProvider:

#     @staticmethod
#     def analyze(request: FailureAnalysisRequest):

#         response = client.responses.create(
#             model=Config.MODEL,
#             input=[
#                 {
#                     "role": "system",
#                     "content": PROMPT
#                 },
#                 {
#                     "role": "user",
#                     "content": f"""
# Test Name:
# {request.testName}

# Error:
# {request.error}

# Logs:
# {request.logs}
# """
#                 }
#             ]
#         )

#         return response
    
from providers.base_provider import BaseProvider

class OpenAIProvider(BaseProvider):

    def analyze(self, request):
        pass