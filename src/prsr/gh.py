"""GitHub CLI (gh) subprocess helpers."""

import logging
import os
import subprocess
from typing import List, Optional

from prsr.errors import GhError

logger = logging.getLogger("prsr")


def run_gh(args: List[str], cwd: Optional[str] = None) -> str:
    """Run ``gh`` with args and return stdout.

    Authentication is whatever ``gh`` already has configured.
    """
    command = ["gh"]
    command.extend(args)
    logger.debug("Running: %s", " ".join(command))

    env = os.environ.copy()
    env["GH_PAGER"] = "cat"
    env["NO_COLOR"] = "1"
    env["GH_NO_UPDATE_NOTIFIER"] = "1"

    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise GhError(
            "gh was not found on PATH. Install the GitHub CLI: https://cli.github.com/"
        ) from exc

    if result.returncode != 0:
        message = result.stderr.strip()
        if message == "":
            message = "gh exited with status %s" % result.returncode
        raise GhError(message)

    return result.stdout


def current_repo() -> str:
    """Return OWNER/NAME for the GitHub repo of the current directory."""
    output = run_gh(["repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"])
    name = output.strip()
    if name == "":
        raise GhError("could not determine the GitHub repository (pass --repo OWNER/NAME)")
    return name


def fetch_pr_diff(pr: str, repo: Optional[str] = None) -> str:
    """Return the unified diff for a pull request."""
    args = ["pr", "diff", str(pr)]
    if repo is not None:
        args.append("--repo")
        args.append(repo)
    return run_gh(args)


def fetch_commit_diff(sha: str, repo: Optional[str] = None) -> str:
    """Return the unified diff for a commit."""
    owner_repo = repo
    if owner_repo is None:
        owner_repo = current_repo()
    path = "repos/%s/commits/%s" % (owner_repo, sha)
    return run_gh(["api", path, "-H", "Accept: application/vnd.github.diff"])


def fetch_compare_diff(base: str, head: str, repo: Optional[str] = None) -> str:
    """Return the unified diff for base...head."""
    owner_repo = repo
    if owner_repo is None:
        owner_repo = current_repo()
    path = "repos/%s/compare/%s...%s" % (owner_repo, base, head)
    return run_gh(["api", path, "-H", "Accept: application/vnd.github.diff"])
