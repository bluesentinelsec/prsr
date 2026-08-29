"""View layer: render a parsed diff as numbered text."""

from typing import Optional

from prsr.model import Diff, DiffLine


def render(diff: Diff, source: Optional[str] = None) -> str:
    """Render a parsed Diff as a git-like view with old/new line numbers."""
    lines = []
    header = "# prsr numbered diff | OLD  NEW  CODE"
    if source is not None and source != "":
        header = header + " | source=" + source
    lines.append(header)

    if len(diff.files) == 0 and len(diff.prelude) == 0:
        lines.append("# (no changes)")
        return "\n".join(lines) + "\n"

    for prelude_line in diff.prelude:
        lines.append(prelude_line)

    width = lineno_width(diff)

    for diff_file in diff.files:
        for header_line in diff_file.header_lines:
            lines.append(header_line)
        for hunk in diff_file.hunks:
            lines.append(hunk.header)
            for item in hunk.lines:
                lines.append(format_body_line(item, width))

    return "\n".join(lines) + "\n"


def lineno_width(diff: Diff) -> int:
    """Column width for line numbers (at least 4)."""
    max_n = 0
    for diff_file in diff.files:
        for hunk in diff_file.hunks:
            for item in hunk.lines:
                if item.old_lineno is not None and item.old_lineno > max_n:
                    max_n = item.old_lineno
                if item.new_lineno is not None and item.new_lineno > max_n:
                    max_n = item.new_lineno
    if max_n < 1:
        return 4
    width = len(str(max_n))
    if width < 4:
        return 4
    return width


def format_number(value: Optional[int], width: int) -> str:
    """Right-align a line number, or spaces when that side has no line."""
    if value is None:
        return " " * width
    return str(value).rjust(width)


def format_body_line(item: DiffLine, width: int) -> str:
    """Format one hunk line as ``OLD NEW <git-line>``."""
    old_s = format_number(item.old_lineno, width)
    new_s = format_number(item.new_lineno, width)
    body = item.prefix + item.text
    return old_s + " " + new_s + " " + body
