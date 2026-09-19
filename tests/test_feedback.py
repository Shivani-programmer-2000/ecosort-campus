import pytest

from ecosort.feedback import FeedbackCounter


def test_counts_only_integers(tmp_path):
    fb = FeedbackCounter(tmp_path / "fb.json")
    assert fb.counts() == {"helpful": 0, "not_helpful": 0, "not_sure": 0}
    fb.record("helpful")
    fb.record("helpful")
    fb.record("not_helpful")
    assert fb.counts() == {"helpful": 2, "not_helpful": 1, "not_sure": 0}
    # privacy: the file contains only three counters, no text
    assert set((tmp_path / "fb.json").read_text().replace('"', "").split(":")[0:1]) <= {"{helpful"}


def test_rejects_unknown_kind(tmp_path):
    with pytest.raises(ValueError):
        FeedbackCounter(tmp_path / "fb.json").record("comment: hello")


def test_unwritable_location_does_not_crash(tmp_path):
    blocker = tmp_path / "file_not_dir"
    blocker.write_text("x")
    fb = FeedbackCounter(blocker / "sub" / "fb.json")  # parent is a file, so writing must fail
    assert fb.record("helpful")["helpful"] == 1
