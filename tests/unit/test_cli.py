"""Unit tests for the prsr CLI parser and main() wiring."""

import io
import logging

import pytest

from prsr import __version__
from prsr.cli import build_parser, main
from prsr.errors import GhError
from tests.unit.sample_diffs import HELLO_DIFF


def test_parser_pr():
    args = build_parser().parse_args(["--pr", "1234"])
    assert args.pr == "1234"
    assert args.commit is None
    assert args.output is None
    assert args.verbose is False
    assert args.color == "auto"


def test_parser_commit_and_output():
    args = build_parser().parse_args(["--commit", "abc123", "-o", "diff.txt", "-v"])
    assert args.commit == "abc123"
    assert args.output == "diff.txt"
    assert args.verbose is True


def test_parser_compare():
    args = build_parser().parse_args(["--base", "main", "--head", "feature", "--repo", "a/b"])
    assert args.base == "main"
    assert args.head == "feature"
    assert args.repo == "a/b"


def test_parser_diff_stdin():
    args = build_parser().parse_args(["--diff", "-"])
    assert args.diff == "-"


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "prsr" in captured.out
    assert __version__ in captured.out


def test_help_lists_core_flags():
    parser = build_parser()
    option_strings = set()
    for action in parser._actions:
        for opt in action.option_strings:
            option_strings.add(opt)
    for flag in (
        "--pr",
        "--commit",
        "--base",
        "--head",
        "--diff",
        "--repo",
        "--output",
        "--verbose",
        "--version",
        "--color",
    ):
        assert flag in option_strings
    assert "-o" in option_strings
    assert "-v" in option_strings


def test_missing_source_errors():
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2


def test_pr_and_commit_together_errors():
    with pytest.raises(SystemExit) as exc:
        main(["--pr", "1", "--commit", "abc"])
    assert exc.value.code == 2


def test_base_without_head_errors():
    with pytest.raises(SystemExit) as exc:
        main(["--base", "main"])
    assert exc.value.code == 2


def test_main_pr_to_stdout(capsys, monkeypatch):
    def fake_render_pr(pr, repo=None, color=False):
        assert pr == "12"
        assert repo is None
        return "# fake numbered diff\n"

    monkeypatch.setattr("prsr.cli.render_pr", fake_render_pr)
    code = main(["--pr", "12"])
    assert code == 0
    captured = capsys.readouterr()
    assert captured.out == "# fake numbered diff\n"


def test_main_output_file(tmp_path, monkeypatch):
    def fake_render_pr(pr, repo=None, color=False):
        assert color is False
        return "# fake numbered diff\n"

    monkeypatch.setattr("prsr.cli.render_pr", fake_render_pr)
    dest = tmp_path / "out.txt"
    code = main(["--pr", "12", "-o", str(dest)])
    assert code == 0
    assert dest.read_text(encoding="utf-8") == "# fake numbered diff\n"


def test_main_diff_file(tmp_path, capsys):
    src = tmp_path / "in.diff"
    src.write_text(HELLO_DIFF, encoding="utf-8")
    code = main(["--diff", str(src)])
    assert code == 0
    captured = capsys.readouterr()
    assert "    1    1 def greet():" in captured.out
    assert "source=file:" in captured.out


def test_main_diff_stdin(capsys, monkeypatch):
    monkeypatch.setattr("prsr.cli.sys.stdin", io.StringIO(HELLO_DIFF))
    code = main(["--diff", "-"])
    assert code == 0
    captured = capsys.readouterr()
    assert "source=stdin" in captured.out
    assert "    4    5     return name" in captured.out


def test_main_commit_dispatches(monkeypatch, capsys):
    def fake_render_commit(sha, repo=None, color=False):
        assert sha == "deadbeef"
        assert repo == "acme/widgets"
        return "# commit diff\n"

    monkeypatch.setattr("prsr.cli.render_commit", fake_render_commit)
    code = main(["--commit", "deadbeef", "--repo", "acme/widgets"])
    assert code == 0
    assert capsys.readouterr().out == "# commit diff\n"


def test_main_compare_dispatches(monkeypatch, capsys):
    def fake_render_compare(base, head, repo=None, color=False):
        assert base == "main"
        assert head == "feature"
        return "# compare diff\n"

    monkeypatch.setattr("prsr.cli.render_compare", fake_render_compare)
    code = main(["--base", "main", "--head", "feature"])
    assert code == 0
    assert capsys.readouterr().out == "# compare diff\n"


def test_main_gh_error_returns_one(monkeypatch, capsys):
    def fake_render_pr(pr, repo=None, color=False):
        raise GhError("nope")

    monkeypatch.setattr("prsr.cli.render_pr", fake_render_pr)
    code = main(["--pr", "1"])
    assert code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "nope" in captured.err


def test_verbose_enables_debug_logging(monkeypatch):
    def fake_render_pr(pr, repo=None, color=False):
        return "# x\n"

    monkeypatch.setattr("prsr.cli.render_pr", fake_render_pr)
    code = main(["--pr", "1", "--verbose"])
    assert code == 0
    assert logging.getLogger().level == logging.DEBUG


def test_parser_color_always():
    args = build_parser().parse_args(["--pr", "1", "--color", "always"])
    assert args.color == "always"


def test_parser_bare_color_means_always():
    args = build_parser().parse_args(["--pr", "1", "--color"])
    assert args.color == "always"


def test_color_always_on_stdout(tmp_path, capsys, monkeypatch):
    src = tmp_path / "in.diff"
    src.write_text(HELLO_DIFF, encoding="utf-8")
    monkeypatch.setattr("prsr.cli.stdout_is_tty", lambda: False)
    monkeypatch.delenv("NO_COLOR", raising=False)
    code = main(["--diff", str(src), "--color", "always"])
    assert code == 0
    out = capsys.readouterr().out
    assert "\033[91m" in out
    assert "\033[32m" in out


def test_color_never_on_tty(tmp_path, capsys, monkeypatch):
    src = tmp_path / "in.diff"
    src.write_text(HELLO_DIFF, encoding="utf-8")
    monkeypatch.setattr("prsr.cli.stdout_is_tty", lambda: True)
    code = main(["--diff", str(src), "--color", "never"])
    assert code == 0
    out = capsys.readouterr().out
    assert "\033[91m" not in out
    assert "\033[32m" not in out


def test_color_auto_on_tty(tmp_path, capsys, monkeypatch):
    src = tmp_path / "in.diff"
    src.write_text(HELLO_DIFF, encoding="utf-8")
    monkeypatch.setattr("prsr.cli.stdout_is_tty", lambda: True)
    monkeypatch.delenv("NO_COLOR", raising=False)
    code = main(["--diff", str(src)])
    assert code == 0
    assert "\033[32m" in capsys.readouterr().out


def test_color_auto_off_for_output_file(tmp_path, monkeypatch):
    src = tmp_path / "in.diff"
    dest = tmp_path / "out.txt"
    src.write_text(HELLO_DIFF, encoding="utf-8")
    monkeypatch.setattr("prsr.cli.stdout_is_tty", lambda: True)
    monkeypatch.delenv("NO_COLOR", raising=False)
    code = main(["--diff", str(src), "-o", str(dest)])
    assert code == 0
    text = dest.read_text(encoding="utf-8")
    assert "\033[91m" not in text
    assert "\033[32m" not in text


def test_color_opt_in_for_output_file(tmp_path, monkeypatch):
    src = tmp_path / "in.diff"
    dest = tmp_path / "out.txt"
    src.write_text(HELLO_DIFF, encoding="utf-8")
    monkeypatch.setattr("prsr.cli.stdout_is_tty", lambda: False)
    monkeypatch.delenv("NO_COLOR", raising=False)
    code = main(["--diff", str(src), "-o", str(dest), "--color"])
    assert code == 0
    text = dest.read_text(encoding="utf-8")
    assert "\033[91m" in text
    assert "\033[32m" in text


def test_no_color_env_disables_auto(tmp_path, capsys, monkeypatch):
    src = tmp_path / "in.diff"
    src.write_text(HELLO_DIFF, encoding="utf-8")
    monkeypatch.setattr("prsr.cli.stdout_is_tty", lambda: True)
    monkeypatch.setenv("NO_COLOR", "1")
    code = main(["--diff", str(src)])
    assert code == 0
    out = capsys.readouterr().out
    assert "\033[91m" not in out
    assert "\033[32m" not in out
