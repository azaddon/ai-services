import json
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from google import genai
from google.genai.errors import ClientError
from services.config import Config
from providers.base_provider import BaseProvider
from providers.response_normalizer import normalize_raw_response  # optional

logger = logging.getLogger(__name__)

# helper to call SDK (keeps single responsibility)
def _call_generate(client, model, parts):
    return client.models.generate_content(
        model=model,
        contents=[{"role": "user", "parts": parts}]
    )

class GeminiProvider(BaseProvider):
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        # models to try: configured first then fallbacks
        self.models = [m for m in ([getattr(Config, "GEMINI_MODEL", None)] + getattr(Config, "MODEL_FALLBACKS", [])) if m]
        # timeout in seconds (convert ms->s if your config uses ms)
        # prefer seconds in config; if AI_TIMEOUT_MS exists, convert:
        if hasattr(Config, "AI_TIMEOUT_MS"):
            self.timeout_s = max(1, int(getattr(Config, "AI_TIMEOUT_MS")) / 1000.0)
        else:
            # default 60 seconds
            self.timeout_s = float(getattr(Config, "AI_TIMEOUT_S", 60))

    def analyze(self, request_obj, rule_result=None, screenshot_data_url=None):
        evidence = getattr(request_obj, "context", request_obj.get("context") if isinstance(request_obj, dict) else {})
        prompt = "FAILURE_ANALYSIS_PROMPT\n\n" + json.dumps(evidence, default=str)
        parts = [{"text": prompt}]
        if screenshot_data_url:
            parts.append({"inline_data": {"mime_type": "image/png", "data": screenshot_data_url.split(",")[1]}})

        last_exc = None
        # Use a single-thread executor per call; it's lightweight for short-lived calls
        for model in self.models:
            try:
                logger.info("Calling Gemini model=%s with timeout=%ss", model, self.timeout_s)
                with ThreadPoolExecutor(max_workers=1) as ex:
                    future = ex.submit(_call_generate, self.client, model, parts)
                    try:
                        resp = future.result(timeout=self.timeout_s)
                        # normalize and return
                        try:
                            return normalize_raw_response(resp)
                        except Exception:
                            # fallback: try to extract text or return string
                            text = getattr(resp, "text", None) or str(resp)
                            return {"analysis_text": text}
                    except FutureTimeout:
                        future.cancel()
                        last_exc = TimeoutError(f"Model {model} timed out after {self.timeout_s} seconds")
                        logger.warning("Gemini model %s timed out", model)
                        # try next model
            except ClientError as e:
                last_exc = e
                logger.warning("Gemini model %s client error: %s", model, e)
            except Exception as e:
                last_exc = e
                logger.exception("Unexpected Gemini error: %s", e)

        # all models failed
        raise RuntimeError(f"All Gemini models failed: {last_exc}")
