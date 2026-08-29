"""Unit tests for the gh subprocess wrapper."""

import subprocess

import pytest

from prsr import gh
from prsr.errors import GhError


class FakeResult:
    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_run_gh_returns_stdout(monkeypatch):
    def fake_run(command, **kwargs):
        assert command[0] == "gh"
        assert command[1] == "pr"
        assert kwargs["encoding"] == "utf-8"
        assert kwargs["env"]["GH_PAGER"] == "cat"
        assert kwargs["env"]["NO_COLOR"] == "1"
        return FakeResult(0, stdout="DIFF TEXT")

    monkeypatch.setattr(subprocess, "run", fake_run)
    output = gh.run_gh(["pr", "diff", "12"])
    assert output == "DIFF TEXT"


def test_run_gh_missing_binary(monkeypatch):
    def fake_run(command, **kwargs):
        raise FileNotFoundError("gh")

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(GhError) as exc:
        gh.run_gh(["pr", "diff", "1"])
    assert "not found" in str(exc.value)


def test_run_gh_nonzero_uses_stderr(monkeypatch):
    def fake_run(command, **kwargs):
        return FakeResult(1, stdout="", stderr="could not find pull request")

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(GhError) as exc:
        gh.run_gh(["pr", "diff", "999"])
    assert "could not find pull request" in str(exc.value)


def test_fetch_pr_diff_passes_repo(monkeypatch):
    seen = []

    def fake_run_gh(args, cwd=None):
        seen.append(list(args))
        return "PRDIFF"

    monkeypatch.setattr(gh, "run_gh", fake_run_gh)
    output = gh.fetch_pr_diff("44", repo="acme/widgets")
    assert output == "PRDIFF"
    assert seen[0] == ["pr", "diff", "44", "--repo", "acme/widgets"]


def test_fetch_commit_diff_uses_api(monkeypatch):
    seen = []

    def fake_run_gh(args, cwd=None):
        seen.append(list(args))
        return "COMMITDIFF"

    monkeypatch.setattr(gh, "run_gh", fake_run_gh)
    output = gh.fetch_commit_diff("abc123", repo="acme/widgets")
    assert output == "COMMITDIFF"
    assert seen[0][0] == "api"
    assert seen[0][1] == "repos/acme/widgets/commits/abc123"
    assert "Accept: application/vnd.github.diff" in seen[0]


def test_fetch_commit_diff_looks_up_repo(monkeypatch):
    def fake_current_repo():
        return "acme/widgets"

    seen = []

    def fake_run_gh(args, cwd=None):
        seen.append(list(args))
        return "COMMITDIFF"

    monkeypatch.setattr(gh, "current_repo", fake_current_repo)
    monkeypatch.setattr(gh, "run_gh", fake_run_gh)
    gh.fetch_commit_diff("abc123")
    assert seen[0][1] == "repos/acme/widgets/commits/abc123"


def test_fetch_compare_diff(monkeypatch):
    seen = []

    def fake_run_gh(args, cwd=None):
        seen.append(list(args))
        return "COMPARE"

    monkeypatch.setattr(gh, "run_gh", fake_run_gh)
    output = gh.fetch_compare_diff("main", "feature", repo="acme/widgets")
    assert output == "COMPARE"
    assert seen[0][1] == "repos/acme/widgets/compare/main...feature"


def test_current_repo_strips(monkeypatch):
    def fake_run_gh(args, cwd=None):
        assert args[0] == "repo"
        return "acme/widgets\n"

    monkeypatch.setattr(gh, "run_gh", fake_run_gh)
    assert gh.current_repo() == "acme/widgets"


def test_current_repo_empty(monkeypatch):
    def fake_run_gh(args, cwd=None):
        return "  \n"

    monkeypatch.setattr(gh, "run_gh", fake_run_gh)
    with pytest.raises(GhError):
        gh.current_repo()
