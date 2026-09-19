"""Anonymous feedback counters. Only three integers are stored: no text, no photos, no user ids."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

KINDS = ("helpful", "not_helpful", "not_sure")


class FeedbackCounter:
    def __init__(self, path: Path):
        self.path = Path(path)

    def counts(self) -> dict:
        try:
            data = json.loads(self.path.read_text())
        except (OSError, json.JSONDecodeError):
            data = {}
        return {k: int(data.get(k, 0)) for k in KINDS}

    def record(self, kind: str) -> dict:
        if kind not in KINDS:
            raise ValueError(f"kind must be one of {KINDS}")
        c = self.counts()
        c[kind] += 1
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=self.path.parent)
            with os.fdopen(fd, "w") as f:
                json.dump(c, f)
            os.replace(tmp, self.path)
        except OSError:  # read-only or full disk on some hosts: never crash the app over a counter
            pass
        return c
