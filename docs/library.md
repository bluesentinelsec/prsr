# Library

Everything the CLI does is available as a library. The CLI is a thin argparse wrapper.

```python
from prsr import render_pr, render_commit, render_compare, render_diff

text = render_pr("1234")
text = render_pr("1234", repo="owner/name")
text = render_commit("abc123")
text = render_compare("main", "feature-branch")
text = render_diff(open("unified.diff").read(), source="file:unified.diff")
text = render_diff(open("unified.diff").read(), color=True)
```

`repo` is optional. When omitted, `gh` uses the GitHub repository of the current working directory.

`color=True` paints ANSI using the same Vim `ft=diff` palette as `--color always`.

## Public names

| Name | Role |
|------|------|
| `render_pr(pr, repo=None, color=False)` | Fetch a PR diff with `gh` and number it |
| `render_commit(sha, repo=None, color=False)` | Fetch a commit diff with `gh` and number it |
| `render_compare(base, head, repo=None, color=False)` | Fetch `base...head` with `gh` and number it |
| `render_diff(diff_text, source=None, color=False)` | Number a unified diff string (no GitHub) |
| `__version__` | Package version string |

## Errors

All library errors subclass `prsr.PrsrError`.

| Exception | When |
|-----------|------|
| `PrsrError` | Base class |
| `GhError` | `gh` missing from `PATH`, or a `gh` command failed |
| `DiffParseError` | The text is not a unified diff `prsr` can parse |

Catch `PrsrError` if you want one handler for CLI-equivalent failures.

## Layers

| Layer | Module | Role |
|-------|--------|------|
| Data model | `prsr.model` | `Diff`, `DiffFile`, `Hunk`, `DiffLine` |
| Logic | `prsr.logic` | Parse unified diffs, assign GitHub line numbers |
| View | `prsr.view` | Render numbered text |
| GitHub | `prsr.gh` | `gh` subprocess calls |
| API | `prsr.api` | The `render_*` functions above |
| CLI | `prsr.cli` | argparse entrypoint |

`DiffLine.old_lineno` and `DiffLine.new_lineno` are 1-based GitHub line numbers. Additions have only NEW; deletions have only OLD; context lines have both.
