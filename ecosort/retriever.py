"""Retrieval step: TF-IDF search over the knowledge base.

This is the whole AI path in offline mode, and the "R" of RAG when a Granite
key is configured.

TF-IDF keeps the prototype dependency-light and fully offline. To upgrade,
swap this class for an embedding-based retriever (for example IBM Granite
embedding models) that exposes the same `search()` method.
"""

from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .knowledge import Chunk

# Words that carry no information about the waste stream.
_STOP = {
    "a", "an", "the", "of", "in", "on", "to", "my", "this", "that", "is", "it", "and", "or", "with",
    "used", "old", "broken", "empty", "waste", "item", "throw", "thrown", "dispose", "where", "what",
    "how", "do", "does", "i", "we", "put", "into", "bin", "some", "piece", "from", "canteen",
    "hostel", "campus", "small", "big", "large", "dirty", "clean", "half", "eaten",
}


def _tokenize(text: str) -> list[str]:
    # "can I recycle..." is a question, but "tin can" is an item, so only drop the verb use.
    text = re.sub(r"\bcan (i|we|you)\b", " ", text.lower())
    tokens = re.findall(r"[a-z]+", text)
    out = []
    for t in tokens:
        if t in _STOP:
            continue
        # light plural normalisation: "batteries" -> "battery", "bottles" -> "bottle"
        if t.endswith("ies") and len(t) > 4:
            t = t[:-3] + "y"
        elif t.endswith("s") and not t.endswith("ss") and len(t) > 3:
            t = t[:-1]
        out.append(t)
    return out


class Retriever:
    def __init__(self, chunks: list[Chunk]):
        if not chunks:
            raise ValueError("Knowledge base is empty")
        self.chunks = chunks
        self._vec = TfidfVectorizer(tokenizer=_tokenize, lowercase=False, token_pattern=None,
                                    ngram_range=(1, 2), sublinear_tf=True)
        self._matrix = self._vec.fit_transform([c.search_text for c in chunks])

    def search(self, query: str, k: int = 3) -> list[tuple[Chunk, float]]:
        """Return up to k (chunk, score) pairs, best first. Score is cosine similarity 0..1."""
        if not _tokenize(query):
            return []
        scores = cosine_similarity(self._vec.transform([query]), self._matrix)[0]
        order = scores.argsort()[::-1][:k]
        return [(self.chunks[i], float(scores[i])) for i in order if scores[i] > 0]
