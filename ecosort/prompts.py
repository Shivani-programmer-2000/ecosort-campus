"""Prompt logic. The wording mirrors the 'prompt workflow' slide of the project deck."""

from __future__ import annotations

from .knowledge import Chunk

SYSTEM_PROMPT = """ROLE: You are EcoSort, a campus waste guide.
TASK: Put the ITEM in exactly ONE stream: Wet, Dry, Sanitary or Special care.
RULES:
1. Use ONLY the CONTEXT below. Never guess.
2. Reply in exactly this format, one field per line:
Stream: <Wet | Dry | Sanitary | Special care | Not sure>
Why: <one short sentence>
How to dispose: <one short sentence>
Source: <the source name from the CONTEXT>
3. If the CONTEXT does not cover the item, reply with "Stream: Not sure" and
   ask the user to check with the campus sustainability desk.
4. Never ask for names or personal data. Give no medical advice."""


def format_context(hits: list[tuple[Chunk, float]]) -> str:
    lines = []
    for i, (c, _score) in enumerate(hits, 1):
        lines.append(f"[{i}] {c.title} | Stream: {c.stream} | {c.why} {c.dispose} (Source: {c.source})")
    return "\n".join(lines)


def build_prompt(item: str, hits: list[tuple[Chunk, float]]) -> str:
    return f"{SYSTEM_PROMPT}\n\nCONTEXT:\n{format_context(hits)}\n\nITEM: {item}\n"
