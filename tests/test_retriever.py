import pytest

from ecosort.config import Settings
from ecosort.knowledge import load_chunks
from ecosort.retriever import Retriever


@pytest.fixture(scope="module")
def retriever():
    return Retriever(load_chunks(Settings().kb_path))


@pytest.mark.parametrize("query,stream", [
    ("banana peel", "Wet"),
    ("plastic bottles", "Dry"),
    ("sanitary pad", "Sanitary"),
    ("batteries", "Special care"),
    ("tin can", "Dry"),
])
def test_top_hit_stream(retriever, query, stream):
    assert retriever.search(query, 1)[0][0].stream == stream


def test_unknown_item_has_no_hits(retriever):
    assert retriever.search("helmet", 3) == []


def test_question_words_are_ignored(retriever):
    assert retriever.search("where can I throw a banana peel", 1)[0][0].stream == "Wet"


def test_empty_query(retriever):
    assert retriever.search("", 3) == []
