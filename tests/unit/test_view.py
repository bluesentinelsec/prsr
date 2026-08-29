"""Unit tests for the numbered-diff view."""

from prsr.logic import parse_unified_diff
from prsr.view import (
    ADDED,
    COMMENT,
    CONSTANT,
    FILE,
    HUNK,
    META,
    REMOVED,
    RESET,
    decide_color,
    lineno_width,
    render,
)
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
        "    1    1 def greet():\n"
        '    2    2     name = "world"\n'
        '-   3          print("hello")\n'
        '+        3     print("hello,")\n'
        "+        4     print(name)\n"
        "    4    5     return name\n"
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
    assert "   99   99 gamma" in text
    assert "- 100      delta" in text
    assert "+      100 DELTA" in text
    assert "+      101 epsilon" in text


def test_render_always_ends_with_newline():
    parsed = parse_unified_diff(HELLO_DIFF)
    text = render(parsed)
    assert text.endswith("\n")


def test_color_paints_additions_green_and_deletions_red():
    parsed = parse_unified_diff(HELLO_DIFF)
    text = render(parsed, color=True)
    assert REMOVED + '-   3          print("hello")' + RESET in text
    assert ADDED + '+        3     print("hello,")' + RESET in text
    assert ADDED + "+        4     print(name)" + RESET in text
    assert "    1    1 def greet():" in text
    assert ADDED + "    1    1 def greet():" not in text
    assert REMOVED + "    1    1 def greet():" not in text


def test_color_follows_vim_diff_groups():
    parsed = parse_unified_diff(HELLO_DIFF)
    text = render(parsed, source="example", color=True)
    assert COMMENT + "# prsr numbered diff | OLD  NEW  CODE | source=example" + RESET in text
    assert FILE + "diff --git a/hello.py b/hello.py" + RESET in text
    assert META + "index 1111111..2222222 100644" + RESET in text
    assert FILE + "--- a/hello.py" + RESET in text
    assert FILE + "+++ b/hello.py" + RESET in text
    assert HUNK + "@@ -1,4 +1,5 @@" + RESET in text
    assert REMOVED + '-   3          print("hello")' + RESET in text
    assert ADDED + '+        3     print("hello,")' + RESET in text


def test_color_binary_line_uses_constant():
    parsed = parse_unified_diff(BINARY_DIFF)
    text = render(parsed, color=True)
    assert CONSTANT + "Binary files a/icon.png and b/icon.png differ" + RESET in text


def test_added_and_deleted_lines_start_with_diff_marker():
    parsed = parse_unified_diff(HELLO_DIFF)
    text = render(parsed)
    found_add = False
    found_del = False
    for line in text.split("\n"):
        if line.startswith("+") and "print" in line:
            found_add = True
        if line.startswith("-") and "print" in line:
            found_del = True
    assert found_add is True
    assert found_del is True


def test_color_off_has_no_ansi():
    parsed = parse_unified_diff(HELLO_DIFF)
    text = render(parsed, color=False)
    assert ADDED not in text
    assert REMOVED not in text
    assert FILE not in text
    assert HUNK not in text
    assert RESET not in text


def test_decide_color_always():
    assert decide_color("always", writing_to_file=True, isatty=False, no_color=True) is True


def test_decide_color_never():
    assert decide_color("never", writing_to_file=False, isatty=True, no_color=False) is False


def test_decide_color_auto_tty_only():
    assert decide_color("auto", writing_to_file=False, isatty=True, no_color=False) is True
    assert decide_color("auto", writing_to_file=False, isatty=False, no_color=False) is False
    assert decide_color("auto", writing_to_file=True, isatty=True, no_color=False) is False
    assert decide_color("auto", writing_to_file=False, isatty=True, no_color=True) is False
