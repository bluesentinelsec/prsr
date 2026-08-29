# prsr

**prsr** (pronounced "pur-sir") is short for **pull request self-review**.

It prints a GitHub-style unified diff **with old and new line numbers preserved**, as plain text, on your machine. You comment in that file. An agent can read the comments and still know exactly which lines you mean — without you posting review comments on a pull request that GitHub thinks you wrote.

[![CI](https://github.com/bluesentinelsec/prsr/actions/workflows/ci.yml/badge.svg)](https://github.com/bluesentinelsec/prsr/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/prsr.svg)](https://pypi.org/project/prsr/)
[![Python versions](https://img.shields.io/pypi/pyversions/prsr.svg)](https://pypi.org/project/prsr/)
[![License](https://img.shields.io/pypi/l/prsr.svg)](https://github.com/bluesentinelsec/prsr/blob/main/LICENSE)

## Why

AI can open a pull request on your behalf. You then review the GitHub diff in the browser, leave line comments, and have AI apply them.

That works, except GitHub shows those comments as you talking to yourself. `prsr` is the same workflow with a local text file instead of the GitHub comment UI.

## Requirements

| | |
|--|--|
| **Python** | 3.8 or newer |
| **GitHub CLI** | [`gh`](https://cli.github.com/) on `PATH`, already authenticated (`gh auth login`) |

`prsr` does not store tokens. It runs `gh` as a subprocess and lets `gh` handle GitHub authentication.

## Install

```bash
pip install prsr
```

From this repository:

```bash
pip install git+https://github.com/bluesentinelsec/prsr.git
```

## Usage

```bash
# numbered diff for a pull request (stdout)
prsr --pr 1234

# write to a file
prsr --pr 1234 -o diff.txt
prsr --pr 1234 > diff.txt

# a single commit
prsr --commit abc123

# compare two refs (branches, tags, or SHAs)
prsr --base main --head feature-branch

# a repo other than the one in the current directory
prsr --repo owner/name --pr 1234

# number a local unified diff (no GitHub call)
prsr --diff unified.diff
git diff main...HEAD | prsr --diff -
```

Also available: `--verbose` / `-v`, `--version`.

## Commenting on the file

Output looks like a normal `git diff`, with two line-number columns in front of each changed line:

```
# prsr numbered diff | OLD  NEW  CODE | source=pr:1234
diff --git a/hello.py b/hello.py
--- a/hello.py
+++ b/hello.py
@@ -1,4 +1,5 @@
   1    1  def greet():
   2    2      name = "world"
   3      -    print("hello")
        3 +    print("hello,")
        4 +    print(name)
   4    5      return name
```

- **OLD** is GitHub's left (before) line number.
- **NEW** is GitHub's right (after) line number.
- Additions have only NEW. Deletions have only OLD. Context lines have both.

Write review notes on their own lines. Leave the numbered source lines alone so line numbers stay aligned:

```
        3 +    print("hello,")
# nit: drop the comma
        4 +    print(name)
```

Then point your agent at the file.

## Library API

Everything the CLI does is available as a library. The CLI is a thin argparse wrapper.

```python
from prsr import render_pr, render_commit, render_compare, render_diff

text = render_pr("1234")
text = render_pr("1234", repo="owner/name")
text = render_commit("abc123")
text = render_compare("main", "feature-branch")
text = render_diff(open("unified.diff").read(), source="file:unified.diff")
```

Layers:

| Layer | Module | Role |
|-------|--------|------|
| Data model | `prsr.model` | `Diff`, `DiffFile`, `Hunk`, `DiffLine` |
| Logic | `prsr.logic` | Parse unified diffs, assign GitHub line numbers |
| View | `prsr.view` | Render numbered text |
| GitHub | `prsr.gh` | `gh` subprocess calls |
| API | `prsr.api` | `render_pr`, `render_commit`, `render_compare`, `render_diff` |
| CLI | `prsr.cli` | argparse entrypoint |

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check src tests
python -m ruff format src tests
python -m mypy
```

## License

[GNU General Public License v2](LICENSE).
