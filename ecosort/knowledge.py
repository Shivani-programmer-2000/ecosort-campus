"""Load the knowledge base (rules + campus guide) into Chunk objects."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

STREAMS = ("Wet", "Dry", "Sanitary", "Special care")


@dataclass(frozen=True)
class Chunk:
    id: str
    stream: str
    title: str
    why: str
    dispose: str
    source: str
    keywords: tuple = field(default_factory=tuple)

    @property
    def search_text(self) -> str:
        return " ".join([self.title, *self.keywords, self.why])


def load_chunks(path: Path) -> list[Chunk]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    chunks = []
    for c in data["chunks"]:
        if c["stream"] not in STREAMS:
            raise ValueError(f"Unknown stream '{c['stream']}' in chunk {c['id']}")
        chunks.append(
            Chunk(
                id=c["id"],
                stream=c["stream"],
                title=c["title"],
                why=c["why"],
                dispose=c["dispose"],
                source=c["source"],
                keywords=tuple(c.get("keywords", [])),
            )
        )
    return chunks


def load_ambiguous(path: Path) -> tuple[str, ...]:
    """Phrases whose stream depends on condition or local rules (e.g. a used tissue).

    The assistant refuses to guess for these and refers the user to the campus desk.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(p.lower() for p in data.get("ambiguous", []))
