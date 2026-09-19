"""Security / secret-leakage tests."""

from __future__ import annotations

from ecosort import EcoSort
from ecosort.config import Settings


def test_settings_repr_hides_secrets():
    s = Settings(watsonx_api_key="SECRET-123", watsonx_project_id="PROJ-456")
    r = repr(s)
    assert "SECRET-123" not in r
    assert "PROJ-456" not in r


def test_startup_failure_note_hides_exception_detail(monkeypatch, caplog):
    def boom(settings):
        raise RuntimeError("secret-detail")
    monkeypatch.setattr("ecosort.pipeline.get_responder", boom)
    caplog.set_level("WARNING")
    bot = EcoSort(Settings(llm_provider="watsonx"))
    note = bot.ask("banana peel").note
    assert note and "secret-detail" not in note
    assert "secret-detail" in caplog.text  # full detail is logged server-side only


def test_cache_never_exceeds_256_entries():
    bot = EcoSort(Settings(llm_provider="offline", llm_daily_cap=0))
    class Fake:
        name = "fake"
        def respond(self, item, hits, prompt):
            return "Stream: Wet\nWhy: x\nHow to dispose: y\nSource: z"
    bot.responder = Fake()
    hits = bot.retriever.search("banana peel", 3)
    for i in range(300):
        bot._generate(f"banana peel {i}", hits, "")
    assert len(bot._cache) == 256
    assert "banana peel 0" not in bot._cache
