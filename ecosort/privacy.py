"""Privacy helpers: the assistant never needs personal data, so strip it if typed."""

from __future__ import annotations

import re

MAX_LEN = 200
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE = re.compile(r"(?<!\d)(?:\+?\d[\s-]?){10,13}(?!\d)")
_PAN = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]", re.I)


def sanitize_query(text: str) -> str:
    """Trim, remove e-mail addresses, phone numbers, and PAN numbers, and cap the length."""
    text = _EMAIL.sub(" ", text or "")
    text = _PHONE.sub(" ", text)
    text = _PAN.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:MAX_LEN]
