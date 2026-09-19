"""Smoke tests for the Streamlit app (no browser, no network)."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def html_blob(at):
    return " ".join(str(getattr(e, "value", "")) for e in at.get("html")) + " ".join(m.value for m in at.markdown)


def new_app():
    at = AppTest.from_file(APP, default_timeout=30)
    at.secrets["LLM_PROVIDER"] = "offline"
    return at.run()


def test_app_loads_without_errors():
    at = new_app()
    assert not at.exception
    assert "Which bin does it go in?" in html_blob(at)


def test_sorting_an_item_shows_the_answer():
    at = new_app()
    at.text_input[0].set_value("tube light")
    at.button[0].click().run()  # the form's "Sort it" button
    assert not at.exception
    blob = html_blob(at)
    assert "Special care" in blob and 'class="bin is-open"' in blob


def test_unknown_item_says_not_sure_and_opens_no_bin():
    at = new_app()
    at.text_input[0].set_value("old phone charger")
    at.button[0].click().run()
    blob = html_blob(at)
    assert "Not sure" in blob and 'class="bin is-open"' not in blob


def test_user_text_is_escaped():
    at = new_app()
    at.text_input[0].set_value("<script>alert(1)</script>")
    at.button[0].click().run()
    assert "<script>alert(1)</script>" not in html_blob(at)
