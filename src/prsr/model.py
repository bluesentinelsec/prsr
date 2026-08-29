"""Data model for a parsed unified diff."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DiffLine:
    """One line inside a hunk.

    prefix is the unified-diff marker: space (context), plus, minus, or
    backslash (the 'No newline at end of file' marker).
    old_lineno and new_lineno are 1-based GitHub line numbers. They are
    None when that side has no line (additions have no old number;
    deletions have no new number).
    """

    prefix: str
    text: str
    old_lineno: Optional[int] = None
    new_lineno: Optional[int] = None


@dataclass
class Hunk:
    """One @@ hunk of a file diff."""

    old_start: int
    old_count: int
    new_start: int
    new_count: int
    header: str
    lines: List[DiffLine] = field(default_factory=list)


@dataclass
class DiffFile:
    """One file in a unified diff."""

    old_path: str = ""
    new_path: str = ""
    header_lines: List[str] = field(default_factory=list)
    hunks: List[Hunk] = field(default_factory=list)
    is_binary: bool = False


@dataclass
class Diff:
    """A complete unified diff (zero or more files)."""

    files: List[DiffFile] = field(default_factory=list)
    prelude: List[str] = field(default_factory=list)
