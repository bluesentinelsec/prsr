"""Command-line interface for prsr."""

import argparse
import logging
import os
import sys
from typing import List, Optional

from prsr._version import __version__
from prsr.api import render_commit, render_compare, render_diff, render_pr
from prsr.errors import PrsrError
from prsr.view import decide_color

logger = logging.getLogger("prsr")


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="prsr",
        description=(
            "Pull request self-review: render a GitHub-style unified diff "
            "with old and new line numbers so you can comment locally."
        ),
        epilog=(
            "examples:\n"
            "  prsr --pr 1234\n"
            "  prsr --pr 1234 -o diff.txt\n"
            "  prsr --commit abc123\n"
            "  prsr --base main --head feature-branch\n"
            "  prsr --diff unified.diff\n"
            "  git diff main...HEAD | prsr --diff -\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--pr",
        metavar="NUMBER",
        help="Pull request number or URL (uses gh pr diff).",
    )
    parser.add_argument(
        "--commit",
        metavar="SHA",
        help="Commit SHA to diff (uses the GitHub commits API via gh).",
    )
    parser.add_argument(
        "--base",
        metavar="REF",
        help="Base branch or SHA for a compare (requires --head).",
    )
    parser.add_argument(
        "--head",
        metavar="REF",
        help="Head branch or SHA for a compare (requires --base).",
    )
    parser.add_argument(
        "--diff",
        metavar="FILE",
        help="Number a local unified diff file. Use - to read stdin.",
    )
    parser.add_argument(
        "--repo",
        metavar="OWNER/NAME",
        help="GitHub repository (default: the repo of the current directory).",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Write the numbered diff to FILE instead of stdout.",
    )
    parser.add_argument(
        "--color",
        nargs="?",
        const="always",
        default="auto",
        choices=["auto", "always", "never"],
        metavar="WHEN",
        help=(
            "Color added lines green and deleted lines red. "
            "WHEN is auto (default: TTY only, not files), always, or never. "
            "Bare --color means always, including -o files."
        ),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging to stderr.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
    )
    return parser


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Require exactly one source of diff input."""
    has_pr = args.pr is not None
    has_commit = args.commit is not None
    has_diff = args.diff is not None
    has_base = args.base is not None
    has_head = args.head is not None
    has_compare = has_base or has_head

    mode_count = 0
    if has_pr:
        mode_count += 1
    if has_commit:
        mode_count += 1
    if has_diff:
        mode_count += 1
    if has_compare:
        mode_count += 1

    if mode_count == 0:
        parser.error("specify --pr, --commit, --diff, or --base and --head")
    if mode_count > 1:
        parser.error("specify only one of --pr, --commit, --diff, or --base/--head")
    if has_compare:
        if not has_base or not has_head:
            parser.error("--base and --head must be used together")


def setup_logging(verbose: bool) -> None:
    """Configure the console logger. Diff text itself always goes to stdout."""
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
        force=True,
    )


def read_local_diff(path: str) -> str:
    """Read a unified diff from a file or stdin."""
    if path == "-":
        return sys.stdin.read()
    try:
        handle = open(path, "r", encoding="utf-8")
    except OSError as exc:
        raise PrsrError("could not read %s: %s" % (path, exc)) from exc
    try:
        return handle.read()
    finally:
        handle.close()


def write_output(path: str, text: str) -> None:
    """Write text to a file, ending with a newline."""
    if not text.endswith("\n"):
        text = text + "\n"
    try:
        handle = open(path, "w", encoding="utf-8")
    except OSError as exc:
        raise PrsrError("could not write %s: %s" % (path, exc)) from exc
    try:
        handle.write(text)
    finally:
        handle.close()


def stdout_is_tty() -> bool:
    """Return True if stdout is an interactive terminal."""
    if not hasattr(sys.stdout, "isatty"):
        return False
    return sys.stdout.isatty()


def no_color_set() -> bool:
    """Return True if the NO_COLOR environment variable is set and non-empty."""
    value = os.environ.get("NO_COLOR")
    if value is None:
        return False
    if value == "":
        return False
    return True


def color_enabled(args: argparse.Namespace) -> bool:
    """Decide whether this CLI run should emit ANSI color."""
    writing_to_file = args.output is not None
    return decide_color(
        args.color,
        writing_to_file,
        stdout_is_tty(),
        no_color_set(),
    )


def run_from_args(args: argparse.Namespace, color: bool = False) -> str:
    """Dispatch to the matching library API call."""
    if args.pr is not None:
        return render_pr(args.pr, repo=args.repo, color=color)
    if args.commit is not None:
        return render_commit(args.commit, repo=args.repo, color=color)
    if args.diff is not None:
        raw = read_local_diff(args.diff)
        if args.diff == "-":
            source = "stdin"
        else:
            source = "file:" + args.diff
        return render_diff(raw, source=source, color=color)
    if args.base is None or args.head is None:
        raise PrsrError("internal error: compare missing base or head")
    return render_compare(args.base, args.head, repo=args.repo, color=color)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entrypoint. Returns a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_args(parser, args)
    setup_logging(args.verbose)

    try:
        text = run_from_args(args, color=color_enabled(args))
    except PrsrError as exc:
        logger.error("%s", exc)
        return 1

    if args.output is not None:
        try:
            write_output(args.output, text)
        except PrsrError as exc:
            logger.error("%s", exc)
            return 1
        logger.info("Wrote %s", args.output)
        return 0

    if not text.endswith("\n"):
        text = text + "\n"
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
