"""Optional photo input (multimodal). Experimental.

Uses a vision-capable model served by a local Ollama install (default: granite3.2-vision).
The image is sent to the model in memory and is never written to disk.
"""

from __future__ import annotations

import base64

from .config import Settings
from .privacy import sanitize_query


class VisionUnavailable(RuntimeError):
    pass


def describe_image(image_bytes: bytes, s: Settings | None = None) -> str:
    """Return a short item name for the photo, e.g. 'banana peel'."""
    s = s or Settings.from_env()
    try:
        import requests

        r = requests.post(
            f"{s.ollama_host.rstrip('/')}/api/generate",
            json={
                "model": s.vision_model,
                "prompt": "Name the single waste item in this photo in one to four words. "
                          "Reply with the item name only.",
                "images": [base64.b64encode(image_bytes).decode()],
                "stream": False,
                "options": {"temperature": 0},
            },
            timeout=120,
        )
        r.raise_for_status()
        return sanitize_query(r.json()["response"]).strip(" .\n")
    except Exception as e:
        raise VisionUnavailable(
            f"Photo mode needs a vision model in Ollama ('{s.vision_model}'). Details: {type(e).__name__}"
        ) from e
