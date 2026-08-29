"""Error types raised by prsr."""


class PrsrError(Exception):
    """Base error raised by prsr."""


class GhError(PrsrError):
    """Raised when a gh command fails or gh is missing."""


class DiffParseError(PrsrError):
    """Raised when a unified diff cannot be parsed."""
