import base64
import binascii
from pathlib import Path

from services.config import Config


class ScreenshotService:
    """Validates screenshot evidence without making a separate LLM call."""

    @classmethod
    def get_data_url(cls, context) -> str | None:
        encoded = context.screenshotBase64
        if not encoded and context.screenshotPath and Config.ALLOW_LOCAL_SCREENSHOT_PATHS:
            path = Path(context.screenshotPath)
            if path.is_file() and path.stat().st_size <= Config.MAX_SCREENSHOT_BYTES:
                encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        if not encoded:
            return None

        if encoded.startswith("data:"):
            try:
                header, encoded = encoded.split(",", 1)
            except ValueError as exc:
                raise ValueError("Invalid screenshot data URL") from exc
            if ";base64" not in header:
                raise ValueError("Screenshot data URL must be base64 encoded")
        try:
            raw = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("screenshotBase64 is not valid base64") from exc
        if not raw or len(raw) > Config.MAX_SCREENSHOT_BYTES:
            raise ValueError("Screenshot is empty or exceeds the configured size limit")

        mime = cls._detect_mime(raw)
        return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"

    @staticmethod
    def _detect_mime(raw: bytes) -> str:
        if raw.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"
        if raw.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if raw.startswith(b"RIFF") and raw[8:12] == b"WEBP":
            return "image/webp"
        raise ValueError("Only PNG, JPEG, and WebP screenshots are supported")
