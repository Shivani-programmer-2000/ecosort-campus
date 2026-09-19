from ecosort.privacy import MAX_LEN, sanitize_query


def test_removes_email_and_phone():
    out = sanitize_query("banana peel, mail me at student@college.edu or call +91 98765 43210")
    assert "@" not in out and "98765" not in out
    assert "banana peel" in out


def test_trims_and_caps_length():
    assert sanitize_query("   tea   bag  ") == "tea bag"
    assert len(sanitize_query("x" * 1000)) == MAX_LEN


def test_none_or_empty():
    assert sanitize_query("") == ""
    assert sanitize_query(None) == ""
