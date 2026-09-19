# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Stack
Python (3.11), Streamlit web app, scikit-learn TF-IDF retrieval, IBM Granite via watsonx.ai or Ollama. No package.json — pure Python project.

## Commands
```bash
# Install
pip install -r requirements-dev.txt

# Run app
streamlit run app.py

# Run all tests
pytest -q

# Run a single test
pytest tests/test_pipeline.py::test_confident_answer_has_source -q

# CLI (offline, no keys needed)
python -m ecosort.cli "banana peel"

# Evaluation (must score 0 confidently-wrong answers or CI fails)
python eval/run_eval.py

# Rebuild static website (docs/index.html must stay in sync with knowledge_base.json; CI checks this)
python scripts/build_site.py
```

## Architecture

```
query → sanitize_query() → Retriever.search() → [confidence gate] → LLM responder → parse_answer() → guardrail → Answer
```

- `ecosort/pipeline.py` — `EcoSort.ask()` is the sole public entry point; `Answer` is the return type.
- `ecosort/knowledge.py` — `Chunk` dataclass; four valid streams are `"Wet"`, `"Dry"`, `"Sanitary"`, `"Special care"`.
- `ecosort/llm.py` — three responders (`OfflineResponder`, `OllamaResponder`, `WatsonxResponder`), selected by `LLM_PROVIDER` env var. App always falls back to `OfflineResponder` on any exception — never raise from the constructor.
- `ecosort/config.py` — `Settings` is a frozen dataclass. `Settings.from_env()` reads env vars first, then Streamlit secrets. Default provider is `"offline"`.
- `docs/index.html` — **generated file** (do not hand-edit). Rebuild with `python scripts/build_site.py` after changing `data/knowledge_base.json` or `site/`.

## Critical Patterns

- **Guardrail in `pipeline.py`**: The LLM-returned stream must exist in the set of streams from retrieved chunks (`allowed`). A hallucinated stream causes the pipeline to return `"Not sure"` instead.
- **`normalise_stream()`**: Only matches if the text *starts with* a stream name — e.g. `"Wet"` matches but `"some Wet stuff"` does not.
- **Ambiguous list**: Items in `data/knowledge_base.json["ambiguous"]` are refused without retrieval — check this list before adding new items.
- **LLM response format**: Must be exactly four lines (`Stream:`, `Why:`, `How to dispose:`, `Source:`). `parse_answer()` is regex-based and case/whitespace tolerant, but field names must match.
- **Daily cap**: `EcoSort._calls` resets at midnight by date comparison; `llm_daily_cap=0` means unlimited.
- **Feedback writes**: `FeedbackCounter.record()` uses an atomic `os.replace(tmp, path)` pattern — do not change this to a direct write.
- **Session limit**: `MAX_PER_SESSION = 60` in `app.py` is a demo guard for public deployment.

## Code Style
- All modules use `from __future__ import annotations`.
- Imports: stdlib → third-party → local (relative `.module`), each group separated by a blank line.
- Dataclasses are `frozen=True` unless mutation is required.
- `# pragma: no cover` on import guards for optional dependencies.
- Exceptions in LLM calls are caught broadly (`except Exception`) and degrade gracefully — do not narrow these.
- No linter config file; follow the style of surrounding code.

## Testing
- Tests use `pytest`; no special markers needed for basic tests.
- `tests/conftest.py` inserts the repo root into `sys.path` — no install step required.
- Instantiate `EcoSort(Settings(llm_provider="offline"))` in fixtures to avoid network calls.
- To test custom LLM behaviour, monkey-patch `bot.responder` with an inline class (see `test_pipeline.py`).
- `eval/run_eval.py` exits with code 1 if any confidently-wrong answer exists — CI treats this as a failure.

## Environment / Secrets
- Copy `.env.example` → `.env`; never commit `.env`.
- Settings can also be set via Streamlit secrets (checked automatically by `config._get()`).
