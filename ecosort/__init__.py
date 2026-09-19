"""EcoSort Campus: a retrieval-based assistant for four-stream waste segregation.

Retrieval-only by default; with an IBM Granite key configured the same pipeline
runs as full Retrieval-Augmented Generation (RAG).
"""

from .pipeline import EcoSort, Answer  # noqa: F401

__version__ = "1.0.0"
