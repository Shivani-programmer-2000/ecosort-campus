"""Settings, read from environment variables (or a local .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:  # optional dependency
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parent.parent


def _get(key: str, default):
    """Read a setting from environment variables, then from Streamlit secrets (Streamlit Cloud)."""
    if key in os.environ:
        return os.environ[key]
    try:  # optional: only available inside a Streamlit app that has secrets configured
        import streamlit as st

        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default


@dataclass(frozen=True)
class Settings:
    # "offline" (no API key needed), "watsonx" (IBM Granite on watsonx.ai) or "ollama" (local Granite)
    llm_provider: str = "offline"
    kb_path: Path = ROOT / "data" / "knowledge_base.json"
    feedback_path: Path = ROOT / "data" / "feedback_counts.json"
    author: str = "NADELLA SHIVANI, JAIN UNIVERSITY"  # shown in the page footer
    top_k: int = 3
    llm_daily_cap: int = 25  # max model calls per day per running app (0 = unlimited). Protects a free quota.
    min_score: float = 0.15  # below this retrieval score, the assistant says "Not sure"

    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    watsonx_api_key: str = field(default="", repr=False)
    watsonx_project_id: str = field(default="", repr=False)
    watsonx_model_id: str = "ibm/granite-4-h-small"

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "granite3.3:8b"
    vision_model: str = "granite3.2-vision"

    @classmethod
    def from_env(cls) -> "Settings":
        g = _get
        d = cls()
        return cls(
            llm_provider=g("LLM_PROVIDER", d.llm_provider).lower(),
            kb_path=Path(g("KB_PATH", str(d.kb_path))),
            feedback_path=Path(g("FEEDBACK_PATH", str(d.feedback_path))),
            author=g("AUTHOR", d.author),
            top_k=int(g("TOP_K", d.top_k)),
            llm_daily_cap=int(g("LLM_DAILY_CAP", d.llm_daily_cap)),
            min_score=float(g("MIN_SCORE", d.min_score)),
            watsonx_url=g("WATSONX_URL", d.watsonx_url),
            watsonx_api_key=g("WATSONX_API_KEY", d.watsonx_api_key),
            watsonx_project_id=g("WATSONX_PROJECT_ID", d.watsonx_project_id),
            watsonx_model_id=g("WATSONX_MODEL_ID", d.watsonx_model_id),
            ollama_host=g("OLLAMA_HOST", d.ollama_host),
            ollama_model=g("OLLAMA_MODEL", d.ollama_model),
            vision_model=g("VISION_MODEL", d.vision_model),
        )
