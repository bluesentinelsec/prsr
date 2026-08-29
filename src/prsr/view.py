"""View layer: render a parsed diff as numbered text."""

from typing import Optional

from prsr.model import Diff, DiffLine

RESET = "\033[0m"

# Vim 9 default diff syntax (ft=diff) ctermfg values, mapped to ANSI
# using :help cterm-colors (NR-16).
ADDED = "\033[32m"  # Added / diffAdded, ctermfg=2 DarkGreen
REMOVED = "\033[91m"  # Removed / diffRemoved, ctermfg=12 Red
FILE = "\033[32m"  # Type / diffFile, ctermfg=2 DarkGreen
HUNK = "\033[1;33m"  # Statement / diffLine, ctermfg=6 Brown, term=bold
META = "\033[35m"  # PreProc / diffIndexLine, ctermfg=5 DarkMagenta
COMMENT = "\033[34m"  # Comment / diffComment, ctermfg=1 DarkBlue
CONSTANT = "\033[31m"  # Constant / binary and "No newline", ctermfg=4 DarkRed


def decide_color(mode: str, writing_to_file: bool, isatty: bool, no_color: bool) -> bool:
    """Return True when ANSI color should be applied.

    auto: color only for a TTY, and never when writing a file or NO_COLOR is set.
    always: color everywhere, including -o files (opt-in).
    never: no color.
    """
    if mode == "always":
        return True
    if mode == "never":
        return False
    if writing_to_file:
        return False
    if no_color:
        return False
    return isatty


def render(diff: Diff, source: Optional[str] = None, color: bool = False) -> str:
    """Render a parsed Diff as a git-like view with old/new line numbers."""
    lines = []
    header = "# prsr numbered diff | OLD  NEW  CODE"
    if source is not None and source != "":
        header = header + " | source=" + source
    lines.append(header)

    if len(diff.files) == 0 and len(diff.prelude) == 0:
        lines.append("# (no changes)")
    else:
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

    if color:
        painted = []
        for line in lines:
            painted.append(colorize_line(line))
        lines = painted

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
    """Format one hunk line as ``+/- OLD NEW text``.

    The unified-diff marker is the first character so editors with a
    built-in diff syntax (Vim ``ft=diff``, GitHub, etc.) color adds and
    deletes without ANSI codes.
    """
    old_s = format_number(item.old_lineno, width)
    new_s = format_number(item.new_lineno, width)
    return item.prefix + old_s + " " + new_s + " " + item.text


def paint(text: str, code: str) -> str:
    """Wrap text in an ANSI color, then reset."""
    return code + text + RESET


def colorize_line(line: str) -> str:
    """Apply Vim default ft=diff colors to one finished output line."""
    if line.startswith("diff ") or line.startswith("Index: ") or line.startswith("==== "):
        return paint(line, FILE)
    if line.startswith("+++ ") or line.startswith("--- "):
        return paint(line, FILE)
    if line.startswith("index "):
        return paint(line, META)
    if line.startswith("@@") or line.startswith("***"):
        return paint(line, HUNK)
    if line.startswith("Binary files ") or line.startswith("Files "):
        return paint(line, CONSTANT)
    if line.startswith("\\"):
        return paint(line, CONSTANT)
    if line.startswith("#"):
        return paint(line, COMMENT)
    if line.startswith("+") or line.startswith(">"):
        return paint(line, ADDED)
    if line.startswith("-") or line.startswith("<"):
        return paint(line, REMOVED)
    return line
