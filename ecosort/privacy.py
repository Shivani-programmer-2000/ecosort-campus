"""Privacy helpers: the assistant never needs personal data, so strip it if typed."""

from __future__ import annotations

import re

MAX_LEN = 200
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE = re.compile(r"(?<!\d)(?:\+?\d[\s-]?){10,13}(?!\d)")


def sanitize_query(text: str) -> str:
    """Trim, remove e-mail addresses and phone numbers, and cap the length."""
    text = _EMAIL.sub(" ", text or "")
    text = _PHONE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:MAX_LEN]
