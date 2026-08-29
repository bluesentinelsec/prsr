"""Logic for parsing unified diffs and assigning line numbers."""

import logging
import re
from typing import Optional, Tuple

from prsr.errors import DiffParseError
from prsr.model import Diff, DiffFile, DiffLine, Hunk

logger = logging.getLogger("prsr")

HUNK_HEADER = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def parse_hunk_header(line: str) -> Hunk:
    """Parse a unified-diff @@ header into a Hunk."""
    match = HUNK_HEADER.match(line)
    if match is None:
        raise DiffParseError("invalid hunk header: %s" % line)

    old_start = int(match.group(1))
    if match.group(2) is None:
        old_count = 1
    else:
        old_count = int(match.group(2))

    new_start = int(match.group(3))
    if match.group(4) is None:
        new_count = 1
    else:
        new_count = int(match.group(4))

    return Hunk(
        old_start=old_start,
        old_count=old_count,
        new_start=new_start,
        new_count=new_count,
        header=line,
    )


def parse_unified_diff(text: str) -> Diff:
    """Parse unified diff text into a Diff with GitHub-style line numbers."""
    diff = Diff()
    current_file: Optional[DiffFile] = None
    current_hunk: Optional[Hunk] = None
    old_cursor = 0
    new_cursor = 0

    lines = text.splitlines()
    for line in lines:
        if current_hunk is not None:
            if hunk_is_complete(current_hunk) and not line.startswith("\\"):
                current_hunk = None

        if line.startswith("diff --git "):
            current_file = DiffFile()
            current_file.header_lines.append(line)
            old_path, new_path = parse_diff_git_paths(line)
            current_file.old_path = old_path
            current_file.new_path = new_path
            diff.files.append(current_file)
            current_hunk = None
            continue

        if line.startswith("@@ "):
            if current_file is None:
                current_file = DiffFile()
                diff.files.append(current_file)
            current_hunk = parse_hunk_header(line)
            current_file.hunks.append(current_hunk)
            old_cursor = current_hunk.old_start
            new_cursor = current_hunk.new_start
            continue

        if current_hunk is not None and is_hunk_body_line(line):
            old_cursor, new_cursor = append_hunk_line(
                current_hunk,
                line,
                old_cursor,
                new_cursor,
            )
            continue

        if current_file is not None:
            current_file.header_lines.append(line)
            update_paths_from_header(current_file, line)
            continue

        diff.prelude.append(line)

    logger.debug("Parsed %s file(s) from unified diff", len(diff.files))
    return diff


def hunk_is_complete(hunk: Hunk) -> bool:
    """Return True once the hunk has consumed old_count and new_count lines."""
    old_seen = 0
    new_seen = 0
    for item in hunk.lines:
        if item.prefix == "\\":
            continue
        if item.prefix == "+":
            new_seen += 1
        elif item.prefix == "-":
            old_seen += 1
        else:
            old_seen += 1
            new_seen += 1
    if old_seen >= hunk.old_count and new_seen >= hunk.new_count:
        return True
    return False


def is_hunk_body_line(line: str) -> bool:
    """Return True if line is a unified-diff hunk body line."""
    if line.startswith("\\"):
        return True
    if line == "":
        return False
    first = line[0]
    if first == "+" or first == "-" or first == " ":
        return True
    return False


def append_hunk_line(
    hunk: Hunk,
    line: str,
    old_cursor: int,
    new_cursor: int,
) -> Tuple[int, int]:
    """Append one hunk body line and return updated old/new cursors."""
    if line.startswith("\\"):
        item = DiffLine(prefix="\\", text=line[1:])
        hunk.lines.append(item)
        return old_cursor, new_cursor

    prefix = line[0]
    text = line[1:]
    if prefix == "+":
        item = DiffLine(
            prefix="+",
            text=text,
            old_lineno=None,
            new_lineno=new_cursor,
        )
        new_cursor += 1
    elif prefix == "-":
        item = DiffLine(
            prefix="-",
            text=text,
            old_lineno=old_cursor,
            new_lineno=None,
        )
        old_cursor += 1
    else:
        item = DiffLine(
            prefix=" ",
            text=text,
            old_lineno=old_cursor,
            new_lineno=new_cursor,
        )
        old_cursor += 1
        new_cursor += 1
    hunk.lines.append(item)
    return old_cursor, new_cursor


def parse_diff_git_paths(line: str) -> Tuple[str, str]:
    """Extract old and new paths from a 'diff --git' line."""
    rest = line[len("diff --git ") :].strip()
    token = " b/"
    idx = rest.find(token)
    if idx == -1:
        return "", ""
    old_raw = rest[:idx]
    new_raw = "b/" + rest[idx + len(token) :]
    return normalize_git_path(old_raw), normalize_git_path(new_raw)


def normalize_git_path(path: str) -> str:
    """Strip a/ or b/ prefixes and surrounding quotes from a git path."""
    path = path.strip()
    if len(path) >= 2 and path[0] == '"' and path[-1] == '"':
        path = path[1:-1]
    if path.startswith("a/") or path.startswith("b/"):
        path = path[2:]
    return path


def update_paths_from_header(diff_file: DiffFile, line: str) -> None:
    """Fill path and binary flags from a file-level header line."""
    if line.startswith("--- "):
        diff_file.old_path = strip_prefix_path(line[4:])
    elif line.startswith("+++ "):
        diff_file.new_path = strip_prefix_path(line[4:])
    elif line.startswith("rename from "):
        diff_file.old_path = line[len("rename from ") :]
    elif line.startswith("rename to "):
        diff_file.new_path = line[len("rename to ") :]
    elif line.startswith("Binary files ") or line.startswith("GIT binary patch"):
        diff_file.is_binary = True


def strip_prefix_path(raw: str) -> str:
    """Parse a ---/+++ path, dropping timestamps and a/ b/ prefixes."""
    raw = raw.split("\t")[0]
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        raw = raw[1:-1]
    if raw.startswith("a/") or raw.startswith("b/"):
        raw = raw[2:]
    return raw
