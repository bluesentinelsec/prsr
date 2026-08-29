"""Unit tests for unified-diff parsing and line-number assignment."""

import pytest

from prsr.errors import DiffParseError
from prsr.logic import parse_hunk_header, parse_unified_diff
from tests.unit.sample_diffs import (
    BINARY_DIFF,
    DELETED_FILE_DIFF,
    HELLO_DIFF,
    MULTI_FILE_DIFF,
    NEW_FILE_DIFF,
    NO_NEWLINE_DIFF,
    OMITTED_COUNTS_DIFF,
    RENAME_DIFF,
    TWO_HUNKS_DIFF,
)


def test_parse_hunk_header_full_counts():
    hunk = parse_hunk_header("@@ -10,6 +12,7 @@ def greet():")
    assert hunk.old_start == 10
    assert hunk.old_count == 6
    assert hunk.new_start == 12
    assert hunk.new_count == 7
    assert hunk.header.startswith("@@ -10,6 +12,7 @@")


def test_parse_hunk_header_omitted_counts_mean_one():
    hunk = parse_hunk_header("@@ -1 +1 @@")
    assert hunk.old_start == 1
    assert hunk.old_count == 1
    assert hunk.new_start == 1
    assert hunk.new_count == 1


def test_parse_hunk_header_empty_old_side():
    hunk = parse_hunk_header("@@ -0,0 +1,2 @@")
    assert hunk.old_start == 0
    assert hunk.old_count == 0
    assert hunk.new_start == 1
    assert hunk.new_count == 2


def test_parse_hunk_header_invalid():
    with pytest.raises(DiffParseError):
        parse_hunk_header("@@ not a hunk @@")


def test_hello_diff_line_numbers():
    parsed = parse_unified_diff(HELLO_DIFF)
    assert len(parsed.files) == 1
    diff_file = parsed.files[0]
    assert diff_file.old_path == "hello.py"
    assert diff_file.new_path == "hello.py"
    assert len(diff_file.hunks) == 1

    hunk = diff_file.hunks[0]
    assert hunk.old_start == 1
    assert hunk.old_count == 4
    assert hunk.new_start == 1
    assert hunk.new_count == 5
    assert len(hunk.lines) == 6

    lines = hunk.lines
    assert lines[0].prefix == " "
    assert lines[0].text == "def greet():"
    assert lines[0].old_lineno == 1
    assert lines[0].new_lineno == 1

    assert lines[1].prefix == " "
    assert lines[1].old_lineno == 2
    assert lines[1].new_lineno == 2

    assert lines[2].prefix == "-"
    assert lines[2].text == '    print("hello")'
    assert lines[2].old_lineno == 3
    assert lines[2].new_lineno is None

    assert lines[3].prefix == "+"
    assert lines[3].text == '    print("hello,")'
    assert lines[3].old_lineno is None
    assert lines[3].new_lineno == 3

    assert lines[4].prefix == "+"
    assert lines[4].text == "    print(name)"
    assert lines[4].old_lineno is None
    assert lines[4].new_lineno == 4

    assert lines[5].prefix == " "
    assert lines[5].text == "    return name"
    assert lines[5].old_lineno == 4
    assert lines[5].new_lineno == 5


def test_new_file_only_has_new_line_numbers():
    parsed = parse_unified_diff(NEW_FILE_DIFF)
    diff_file = parsed.files[0]
    assert diff_file.old_path == "/dev/null"
    assert diff_file.new_path == "new.py"
    lines = diff_file.hunks[0].lines
    assert len(lines) == 2
    assert lines[0].prefix == "+"
    assert lines[0].old_lineno is None
    assert lines[0].new_lineno == 1
    assert lines[1].old_lineno is None
    assert lines[1].new_lineno == 2


def test_deleted_file_only_has_old_line_numbers():
    parsed = parse_unified_diff(DELETED_FILE_DIFF)
    diff_file = parsed.files[0]
    assert diff_file.old_path == "old.py"
    assert diff_file.new_path == "/dev/null"
    lines = diff_file.hunks[0].lines
    assert len(lines) == 2
    assert lines[0].prefix == "-"
    assert lines[0].old_lineno == 1
    assert lines[0].new_lineno is None
    assert lines[1].old_lineno == 2
    assert lines[1].new_lineno is None


def test_binary_file_has_no_hunks():
    parsed = parse_unified_diff(BINARY_DIFF)
    diff_file = parsed.files[0]
    assert diff_file.is_binary is True
    assert diff_file.new_path == "icon.png"
    assert diff_file.hunks == []


def test_no_newline_marker_has_no_line_numbers():
    parsed = parse_unified_diff(NO_NEWLINE_DIFF)
    lines = parsed.files[0].hunks[0].lines
    assert len(lines) == 3
    assert lines[0].prefix == "-"
    assert lines[0].old_lineno == 1
    assert lines[1].prefix == "+"
    assert lines[1].new_lineno == 1
    assert lines[2].prefix == "\\"
    assert lines[2].text == " No newline at end of file"
    assert lines[2].old_lineno is None
    assert lines[2].new_lineno is None


def test_multi_file_diff():
    parsed = parse_unified_diff(MULTI_FILE_DIFF)
    assert len(parsed.files) == 2
    assert parsed.files[0].new_path == "a.txt"
    assert parsed.files[1].new_path == "b.txt"
    a_lines = parsed.files[0].hunks[0].lines
    assert a_lines[0].old_lineno == 1
    assert a_lines[0].new_lineno == 1
    assert a_lines[1].prefix == "+"
    assert a_lines[1].new_lineno == 2
    b_lines = parsed.files[1].hunks[0].lines
    assert b_lines[1].prefix == "-"
    assert b_lines[1].old_lineno == 2


def test_rename_paths():
    parsed = parse_unified_diff(RENAME_DIFF)
    diff_file = parsed.files[0]
    assert diff_file.old_path == "old_name.py"
    assert diff_file.new_path == "new_name.py"
    lines = diff_file.hunks[0].lines
    assert lines[1].old_lineno == 2
    assert lines[1].new_lineno is None
    assert lines[2].old_lineno is None
    assert lines[2].new_lineno == 2
    assert lines[3].old_lineno == 3
    assert lines[3].new_lineno == 3


def test_omitted_hunk_counts():
    parsed = parse_unified_diff(OMITTED_COUNTS_DIFF)
    hunk = parsed.files[0].hunks[0]
    assert hunk.old_count == 1
    assert hunk.new_count == 1
    assert len(hunk.lines) == 2


def test_two_hunks_keep_independent_cursors():
    parsed = parse_unified_diff(TWO_HUNKS_DIFF)
    hunks = parsed.files[0].hunks
    assert len(hunks) == 2
    assert hunks[0].lines[0].old_lineno == 1
    assert hunks[0].lines[1].new_lineno == 1
    assert hunks[1].lines[0].old_lineno == 99
    assert hunks[1].lines[0].new_lineno == 99
    assert hunks[1].lines[1].old_lineno == 100
    assert hunks[1].lines[2].new_lineno == 100
    assert hunks[1].lines[3].new_lineno == 101


def test_empty_diff():
    parsed = parse_unified_diff("")
    assert parsed.files == []
    assert parsed.prelude == []


def test_empty_file_only_newline():
    parsed = parse_unified_diff("\n")
    assert parsed.files == []
    assert parsed.prelude == [""]
