"""prsr: pull request self-review with numbered local diffs."""

from prsr._version import __version__
from prsr.api import render_commit, render_compare, render_diff, render_pr
from prsr.errors import DiffParseError, GhError, PrsrError
from prsr.model import Diff, DiffFile, DiffLine, Hunk

__all__ = [
    "Diff",
    "DiffFile",
    "DiffLine",
    "DiffParseError",
    "GhError",
    "Hunk",
    "PrsrError",
    "__version__",
    "render_commit",
    "render_compare",
    "render_diff",
    "render_pr",
]
