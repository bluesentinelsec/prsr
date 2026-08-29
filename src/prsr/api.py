"""Library API for rendering numbered diffs."""

import logging
from typing import Optional

from prsr import gh
from prsr.logic import parse_unified_diff
from prsr.view import render

logger = logging.getLogger("prsr")


def render_diff(diff_text: str, source: Optional[str] = None) -> str:
    """Parse unified diff text and return the numbered view.

    This does not call gh. Use it to number a local ``git diff`` or a
    file saved from GitHub.
    """
    parsed = parse_unified_diff(diff_text)
    return render(parsed, source=source)


def render_pr(pr: str, repo: Optional[str] = None) -> str:
    """Fetch a pull request diff with gh and return the numbered view."""
    logger.info("Fetching pull request %s", pr)
    raw = gh.fetch_pr_diff(pr, repo=repo)
    source = "pr:%s" % pr
    if repo is not None:
        source = source + " repo:" + repo
    return render_diff(raw, source=source)


def render_commit(sha: str, repo: Optional[str] = None) -> str:
    """Fetch a commit diff with gh and return the numbered view."""
    logger.info("Fetching commit %s", sha)
    raw = gh.fetch_commit_diff(sha, repo=repo)
    source = "commit:%s" % sha
    if repo is not None:
        source = source + " repo:" + repo
    return render_diff(raw, source=source)


def render_compare(base: str, head: str, repo: Optional[str] = None) -> str:
    """Fetch a base...head compare diff with gh and return the numbered view."""
    logger.info("Fetching compare %s...%s", base, head)
    raw = gh.fetch_compare_diff(base, head, repo=repo)
    source = "compare:%s...%s" % (base, head)
    if repo is not None:
        source = source + " repo:" + repo
    return render_diff(raw, source=source)
