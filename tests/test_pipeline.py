import pytest

from ecosort import EcoSort
from ecosort.config import Settings
from ecosort.pipeline import normalise_stream, parse_answer


@pytest.fixture()
def bot():
    return EcoSort(Settings(llm_provider="offline"))


def test_confident_answer_has_source(bot):
    a = bot.ask("banana peel")
    assert a.stream == "Wet" and a.confident and a.source and a.evidence


def test_unknown_item_says_not_sure(bot):
    a = bot.ask("old phone charger")
    assert a.stream == "Not sure" and not a.confident
    assert "sustainability desk" in a.dispose


def test_ambiguous_item_says_not_sure(bot):
    assert bot.ask("used tissue paper").stream == "Not sure"


def test_empty_input(bot):
    assert bot.ask("   ").stream == "Not sure"


def test_personal_data_is_stripped(bot):
    a = bot.ask("banana peel john@example.com 9876543210")
    assert "@" not in a.item and "9876543210" not in a.item


def test_guardrail_rejects_stream_not_in_evidence(bot):
    class Liar:
        name = "fake"

        def respond(self, item, hits, prompt):
            return "Stream: Sanitary\nWhy: made up\nHow to dispose: made up\nSource: made up"

    bot.responder = Liar()
    assert bot.ask("banana peel").stream == "Not sure"


def test_model_error_falls_back_to_offline(bot):
    class Broken:
        name = "broken"

        def respond(self, item, hits, prompt):
            raise ConnectionError("no network")

    bot.responder = Broken()
    a = bot.ask("banana peel")
    assert a.stream == "Wet" and "failed" in a.note


def test_unparsable_model_output_is_not_sure(bot):
    class Rambler:
        name = "rambler"

        def respond(self, item, hits, prompt):
            return "I think it might go somewhere."

    bot.responder = Rambler()
    assert bot.ask("banana peel").stream == "Not sure"


def test_watsonx_without_keys_degrades_to_offline():
    b = EcoSort(Settings(llm_provider="watsonx"))
    assert b.mode == "offline" and b.ask("banana peel").stream == "Wet"


@pytest.mark.parametrize("text,expected", [
    ("Wet", "Wet"), ("special care", "Special care"), ("Special-care waste", "Special care"),
    ("DRY.", "Dry"), ("Not sure", "Not sure"), ("banana", "Not sure"),
])
def test_normalise_stream(text, expected):
    assert normalise_stream(text) == expected


def test_parse_answer():
    p = parse_answer("Stream: Dry\nWhy: Plastic is recyclable.\nHow to dispose: Dry bin.\nSource: SWM Rules")
    assert p["stream"] == "Dry" and p["source"] == "SWM Rules" and p["how to dispose"] == "Dry bin."
