"""Unit tests for the library API (gh calls mocked)."""

from prsr.api import render_commit, render_compare, render_diff, render_pr
from tests.unit.sample_diffs import HELLO_DIFF


def test_render_diff_numbers_local_text():
    text = render_diff(HELLO_DIFF, source="file:hello.diff")
    assert text.startswith("# prsr numbered diff | OLD  NEW  CODE | source=file:hello.diff\n")
    assert "    1    1 def greet():" in text
    assert '-   3          print("hello")' in text


def test_render_pr_uses_gh(monkeypatch):
    def fake_fetch(pr, repo=None):
        assert pr == "12"
        assert repo == "acme/widgets"
        return HELLO_DIFF

    monkeypatch.setattr("prsr.api.gh.fetch_pr_diff", fake_fetch)
    text = render_pr("12", repo="acme/widgets")
    assert "source=pr:12 repo:acme/widgets" in text.split("\n")[0]
    assert "    4    5     return name" in text


def test_render_commit_uses_gh(monkeypatch):
    def fake_fetch(sha, repo=None):
        assert sha == "abc123"
        assert repo is None
        return HELLO_DIFF

    monkeypatch.setattr("prsr.api.gh.fetch_commit_diff", fake_fetch)
    text = render_commit("abc123")
    assert "source=commit:abc123" in text.split("\n")[0]


def test_render_compare_uses_gh(monkeypatch):
    def fake_fetch(base, head, repo=None):
        assert base == "main"
        assert head == "feature"
        return HELLO_DIFF

    monkeypatch.setattr("prsr.api.gh.fetch_compare_diff", fake_fetch)
    text = render_compare("main", "feature")
    assert "source=compare:main...feature" in text.split("\n")[0]
