"""The full EcoSort pipeline: sanitise -> retrieve -> confidence gate -> generate -> validate."""

from __future__ import annotations

import datetime as _dt
import logging
import re
from dataclasses import dataclass, field

from .config import Settings
from .knowledge import STREAMS, load_ambiguous, load_chunks
from .llm import OfflineResponder, get_responder
from .privacy import sanitize_query
from .prompts import build_prompt
from .retriever import Retriever

NOT_SURE = "Not sure"
_FIELD = re.compile(r"^\s*(stream|why|how to dispose|source)\s*:\s*(.+?)\s*$", re.I | re.M)


@dataclass
class Answer:
    item: str
    stream: str
    why: str
    dispose: str
    source: str
    confident: bool
    score: float = 0.0
    evidence: list[str] = field(default_factory=list)  # titles of retrieved passages
    note: str = ""  # e.g. "LLM unavailable, used offline mode"

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def normalise_stream(text: str) -> str:
    t = re.sub(r"[^a-z ]", " ", text.lower()).strip()
    t = re.sub(r"\s+", " ", t)
    for s in STREAMS:
        if t.startswith(s.lower()):
            return s
    if t.startswith("special"):
        return "Special care"
    return NOT_SURE


def parse_answer(raw: str) -> dict:
    """Parse the 4-line model reply. Missing fields come back as empty strings."""
    out = {"stream": "", "why": "", "how to dispose": "", "source": ""}
    for key, val in _FIELD.findall(raw or ""):
        out.setdefault(key.lower(), val)
        if not out[key.lower()]:
            out[key.lower()] = val
    return out


def _not_sure(item: str, score: float = 0.0, evidence=None, note: str = "") -> Answer:
    return Answer(
        item=item,
        stream=NOT_SURE,
        why="I could not find this item in my sources, so I will not guess.",
        dispose="Please ask the campus sustainability desk.",
        source="-",
        confident=False,
        score=score,
        evidence=evidence or [],
        note=note,
    )


class EcoSort:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings.from_env()
        self.retriever = Retriever(load_chunks(self.settings.kb_path))
        self._ambiguous = load_ambiguous(self.settings.kb_path)
        self._note = ""
        self._cache: dict[str, str] = {}  # item -> raw model reply, so repeats cost no tokens
        self._calls_day, self._calls = _dt.date.today(), 0
        try:
            self.responder = get_responder(self.settings)
        except Exception as e:  # missing keys / SDK / bad model id / no network: degrade gracefully
            self.responder = OfflineResponder()
            self._note = "AI model unavailable; using the offline knowledge base."
            logging.getLogger(__name__).warning(
                "Could not start %s", self.settings.llm_provider, exc_info=True
            )

    @property
    def mode(self) -> str:
        return self.responder.name

    def _quota_left(self) -> bool:
        today = _dt.date.today()
        if today != self._calls_day:
            self._calls_day, self._calls = today, 0
        cap = self.settings.llm_daily_cap
        return cap <= 0 or self._calls < cap

    def _generate(self, item, hits, note):
        """Call the model (with cache and daily cap); always fall back to the offline answer."""
        offline = OfflineResponder()
        if isinstance(self.responder, OfflineResponder):
            return offline.respond(item, hits, ""), note
        key = item.lower()
        if key in self._cache:
            return self._cache[key], note
        if not self._quota_left():
            return offline.respond(item, hits, ""), "Daily model quota reached; answered from the knowledge base only."
        try:
            self._calls += 1
            raw = self.responder.respond(item, hits, build_prompt(item, hits))
            if len(self._cache) >= 256:
                self._cache.pop(next(iter(self._cache)))
            self._cache[key] = raw
            return raw, note
        except Exception as e:  # network / model error
            return offline.respond(item, hits, ""), f"Model call failed ({type(e).__name__}); answered from the knowledge base only."

    def ask(self, query: str) -> Answer:
        item = sanitize_query(query)
        if not item:
            return _not_sure(item, note="Please type the name of an item.")

        low = item.lower()
        if any(p in low for p in self._ambiguous):
            a = _not_sure(item)
            a.why = ("Where this goes depends on its condition (for example soiled or plastic-lined) "
                     "or on local rules, so I will not guess.")
            return a

        hits = self.retriever.search(item, self.settings.top_k)
        if not hits or hits[0][1] < self.settings.min_score:
            return _not_sure(item, hits[0][1] if hits else 0.0, [h[0].title for h in hits])

        evidence = [c.title for c, _ in hits]
        note = self._note
        raw, note = self._generate(item, hits, note)

        f = parse_answer(raw)
        stream = normalise_stream(f["stream"])
        allowed = {c.stream for c, _ in hits}
        if stream == NOT_SURE or stream not in allowed:  # guardrail: must agree with retrieved evidence
            return _not_sure(item, hits[0][1], evidence, note)

        top = hits[0][0]
        return Answer(
            item=item,
            stream=stream,
            why=f["why"] or top.why,
            dispose=f["how to dispose"] or top.dispose,
            source=f["source"] or top.source,
            confident=True,
            score=round(hits[0][1], 3),
            evidence=evidence,
            note=note,
        )
