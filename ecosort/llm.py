"""Generation step: pluggable 'responders' that turn retrieved context into an answer.

* OfflineResponder : no model, no key. Answers straight from the top retrieved chunk.
* OllamaResponder  : runs an IBM Granite model locally through Ollama.
* WatsonxResponder : runs an IBM Granite model on IBM watsonx.ai.

Each responder returns text in the 4-line format defined in prompts.SYSTEM_PROMPT.
"""

from __future__ import annotations

from .config import Settings
from .knowledge import Chunk


class OfflineResponder:
    name = "offline"

    def respond(self, item: str, hits: list[tuple[Chunk, float]], prompt: str) -> str:
        c = hits[0][0]
        return f"Stream: {c.stream}\nWhy: {c.why}\nHow to dispose: {c.dispose}\nSource: {c.source}"


class OllamaResponder:
    def __init__(self, s: Settings):
        self.host, self.model = s.ollama_host.rstrip("/"), s.ollama_model
        self.name = f"ollama:{self.model}"

    def respond(self, item: str, hits: list[tuple[Chunk, float]], prompt: str) -> str:
        import requests

        r = requests.post(
            f"{self.host}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False, "options": {"temperature": 0}},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["response"]


class WatsonxResponder:
    def __init__(self, s: Settings):
        try:
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("Install the watsonx SDK: pip install ibm-watsonx-ai") from e
        if not (s.watsonx_api_key and s.watsonx_project_id):
            raise RuntimeError("Set WATSONX_API_KEY and WATSONX_PROJECT_ID in your .env file")
        self.name = f"watsonx:{s.watsonx_model_id}"
        self._model = ModelInference(
            model_id=s.watsonx_model_id,
            credentials=Credentials(url=s.watsonx_url, api_key=s.watsonx_api_key),
            project_id=s.watsonx_project_id,
            params={"decoding_method": "greedy", "max_new_tokens": 200},
        )

    def respond(self, item: str, hits: list[tuple[Chunk, float]], prompt: str) -> str:
        return self._model.generate_text(prompt=prompt)


def get_responder(s: Settings):
    if s.llm_provider == "watsonx":
        return WatsonxResponder(s)
    if s.llm_provider == "ollama":
        return OllamaResponder(s)
    return OfflineResponder()
