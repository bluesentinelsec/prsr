"""Unit tests for the numbered-diff view."""

from prsr.logic import parse_unified_diff
from prsr.view import lineno_width, render
from tests.unit.sample_diffs import BINARY_DIFF, HELLO_DIFF, TWO_HUNKS_DIFF


def test_hello_render_matches_expected_gutter():
    parsed = parse_unified_diff(HELLO_DIFF)
    text = render(parsed, source="example")
    expected = (
        "# prsr numbered diff | OLD  NEW  CODE | source=example\n"
        "diff --git a/hello.py b/hello.py\n"
        "index 1111111..2222222 100644\n"
        "--- a/hello.py\n"
        "+++ b/hello.py\n"
        "@@ -1,4 +1,5 @@\n"
        "   1    1  def greet():\n"
        '   2    2      name = "world"\n'
        '   3      -    print("hello")\n'
        '        3 +    print("hello,")\n'
        "        4 +    print(name)\n"
        "   4    5      return name\n"
    )
    assert text == expected


def test_empty_render_notes_no_changes():
    parsed = parse_unified_diff("")
    text = render(parsed)
    assert text == "# prsr numbered diff | OLD  NEW  CODE\n# (no changes)\n"


def test_binary_render_keeps_git_headers():
    parsed = parse_unified_diff(BINARY_DIFF)
    text = render(parsed, source="pr:1")
    assert "Binary files a/icon.png and b/icon.png differ\n" in text
    assert "@@" not in text


def test_width_grows_for_large_line_numbers():
    parsed = parse_unified_diff(TWO_HUNKS_DIFF)
    assert lineno_width(parsed) == 4
    text = render(parsed)
    assert "  99   99  gamma" in text
    assert " 100      -delta" in text
    assert "      100 +DELTA" in text
    assert "      101 +epsilon" in text


def test_render_always_ends_with_newline():
    parsed = parse_unified_diff(HELLO_DIFF)
    text = render(parsed)
    assert text.endswith("\n")
