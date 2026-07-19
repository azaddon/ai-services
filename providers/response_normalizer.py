# providers/response_normalizer.py
import json
import logging
import re
from typing import Any, Dict

logger = logging.getLogger(__name__)

def normalize_raw_response(raw: Any) -> Dict[str, Any]:
    """
    Normalize SDK responses, strings (possibly code-fenced JSON), or dicts.
    Always returns a dict.
    """
    # If already dict-like
    if isinstance(raw, dict):
        return raw

    # If object with .text attribute (SDK)
    text = None
    try:
        text = getattr(raw, "text", None)
    except Exception:
        text = None

    if not text:
        # fallback to string conversion
        text = str(raw)

    cleaned = text.strip()
    # remove triple backticks if present
    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned.strip("`").strip()
    # remove leading language tag like ```json
    cleaned = re.sub(r"^```?json\s*", "", cleaned, flags=re.IGNORECASE)

    # try parse JSON
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
        # if parsed is list or primitive, wrap it
        return {"analysis": parsed}
    except Exception:
        # not JSON, return as text field
        return {"analysis_text": cleaned[:20000]}  # truncate to avoid huge payloads

def map_to_failure_response(raw: Any) -> Dict[str, Any]:
    """
    Map normalized raw response to FailureAnalysisResponse schema:
    { summary, rootCause, recommendation, confidence }
    """
    # Ensure we have a dict
    if not isinstance(raw, dict):
        raw = normalize_raw_response(raw)

    # Try common keys first
    summary = raw.get("summary") or raw.get("analysis_summary") or raw.get("title") or raw.get("analysis_text")
    root = raw.get("rootCause") or raw.get("root_cause") or raw.get("cause")
    recommendation = raw.get("recommendation") or raw.get("actionableSteps") or raw.get("fix")
    confidence = raw.get("confidence") or raw.get("confidence_score") or raw.get("score")

    # If confidence is string/float, normalize to int 0-100
    try:
        if confidence is not None:
            confidence = int(float(confidence))
            if confidence < 0 or confidence > 100:
                confidence = None
    except Exception:
        confidence = None

    # Heuristic fallback: try to extract from text if missing
    if not summary and "analysis" in raw and isinstance(raw["analysis"], str):
        text = raw["analysis"]
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        summary = " ".join(sentences[:2]) if sentences else text[:300]

    # Final defaults
    if not summary:
        summary = "No summary available"
    if not root:
        root = "Unknown"
    if not recommendation:
        recommendation = "Investigate logs, assertions, and page state; re-run with debug screenshots."
    if confidence is None:
        confidence = 50

    return {
        "summary": summary,
        "rootCause": root,
        "recommendation": recommendation,
        "confidence": int(confidence)
    }
