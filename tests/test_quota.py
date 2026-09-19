from ecosort import EcoSort
from ecosort.config import Settings


class CountingModel:
    name = "counting"

    def __init__(self):
        self.calls = 0

    def respond(self, item, hits, prompt):
        self.calls += 1
        c = hits[0][0]
        return f"Stream: {c.stream}\nWhy: {c.why}\nHow to dispose: {c.dispose}\nSource: {c.source}"


def make(cap):
    bot = EcoSort(Settings(llm_provider="offline", llm_daily_cap=cap))
    bot.responder = CountingModel()
    return bot


def test_repeated_items_are_cached():
    bot = make(cap=25)
    for _ in range(5):
        assert bot.ask("banana peel").stream == "Wet"
    assert bot.responder.calls == 1


def test_daily_cap_falls_back_to_offline():
    bot = make(cap=2)
    for q in ["banana peel", "tube light", "plastic bottle", "sanitary pad"]:
        assert bot.ask(q).stream != "Not sure"
    assert bot.responder.calls == 2
    assert "quota" in bot.ask("battery").note.lower()


def test_cap_zero_means_unlimited():
    bot = make(cap=0)
    for q in ["banana peel", "tube light", "plastic bottle", "sanitary pad"]:
        bot.ask(q)
    assert bot.responder.calls == 4


def test_bad_provider_setup_never_crashes(monkeypatch):
    import ecosort.pipeline as pl

    def boom(_settings):
        raise ValueError("invalid API key")

    monkeypatch.setattr(pl, "get_responder", boom)
    b = EcoSort(Settings(llm_provider="watsonx"))
    assert b.mode == "offline" and "offline" in b._note.lower()
    assert b.ask("banana peel").stream == "Wet"
