from email.mime import image
import os
import base64
from unittest import result
from urllib import request
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ScreenshotService:

    @staticmethod
    def encode_image(path: str):

        if not path:
            return None

        if not os.path.exists(path):
            return None

        with open(path, "rb") as image:
            return base64.b64encode(image.read()).decode("utf-8")


    @staticmethod
    def analyze(request):
        print("===== ScreenshotService =====")

        print("Request:", request)

        print("Context:", request.context)

        print("Screenshot Path:", request.context.screenshotPath)
        if not request.context.screenshotPath:
            print("Screenshot path is EMPTY")
            return None
        print("Exists:", os.path.exists(request.context.screenshotPath))

        if not os.path.exists(request.context.screenshotPath):
            print("Screenshot file NOT FOUND")
            return None

        print("\n========== SCREENSHOT ANALYSIS START ==========")

        print("Screenshot path:", request.context.screenshotPath)

        image = ScreenshotService.encode_image(request.context.screenshotPath)

        print("Image encoded:", image is not None)

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
You are an expert Selenium and Playwright automation engineer.

You MUST answer only from the screenshot.

Do NOT use any logs or stack trace.

Describe exactly:

1. What page is open?
2. Which menu is selected?
3. Is a user logged in?
4. What buttons are visible?
5. What text is visible in the page?
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image}"
                            }
                        }
                    ]
                }
            ]
        )

        result = response.choices[0].message.content
        print("GPT Screenshot Result:")
        print(result)

        print("========== SCREENSHOT ANALYSIS END ==========\n")

        return result