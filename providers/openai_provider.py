# providers/openai_provider.py
import json, logging, time
import openai
from services.config import Config
from providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)
openai.api_key = Config.OPENAI_KEY

class OpenAIProvider(BaseProvider):
    def __init__(self):
        self.models = [Config.OPENAI_MODEL] + Config.MODEL_FALLBACKS

    def _normalize_response(self, resp):
        # adapt to OpenAI response shape
        try:
            text = resp["choices"][0]["message"]["content"]
            # try parse JSON
            try:
                return json.loads(text)
            except:
                return {"analysis_text": text}
        except Exception:
            return {"analysis_text": str(resp)}

    def analyze(self, request, rule_result=None, screenshot_data_url=None) -> dict:
        evidence = request.context.model_dump(exclude={"screenshotBase64","screenshotPath","videoPath"}, exclude_none=True)
        evidence["ruleEngineHint"] = rule_result
        prompt = "YOUR_PROMPT_PREFIX\n\n" + json.dumps(evidence, default=str)
        for model in self.models:
            try:
                logger.info("OpenAI call model=%s", model)
                resp = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role":"user","content":prompt}],
                    timeout=Config.AI_TIMEOUT_MS/1000
                )
                return self._normalize_response(resp)
            except Exception as e:
                logger.warning("OpenAI model %s failed: %s", model, e)
        raise RuntimeError("All OpenAI models failed")
