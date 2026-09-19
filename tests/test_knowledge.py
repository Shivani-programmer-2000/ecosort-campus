from ecosort.config import Settings
from ecosort.knowledge import STREAMS, load_chunks


def test_every_stream_is_covered_and_sourced():
    chunks = load_chunks(Settings().kb_path)
    assert {c.stream for c in chunks} == set(STREAMS)
    assert all(c.source and c.why and c.dispose for c in chunks)
    assert len({c.id for c in chunks}) == len(chunks)
