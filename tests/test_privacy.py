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


def test_removes_pan_number():
    out = sanitize_query("throw away ABCDE1234F with the dry waste")
    assert "ABCDE1234F" not in out
    assert "dry waste" in out


def test_removes_pan_case_insensitive():
    out = sanitize_query("abcde1234f is my PAN")
    assert "abcde1234f" not in out


def test_pan_partial_match_not_stripped():
    # Only 9-char near-matches (too short) should not be stripped
    out = sanitize_query("ABCDE1234")
    assert "ABCDE1234" in out
