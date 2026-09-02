# prsr

**prsr** (pronounced "pur-sir") is short for **pull request self-review**.

It prints a GitHub-style unified diff **with old and new line numbers preserved**, as plain text, on your machine. You comment in that file. An agent can read the comments and still know exactly which lines you mean — without you posting review comments on a pull request that GitHub thinks you wrote.

[![CI](https://github.com/bluesentinelsec/prsr/actions/workflows/ci.yml/badge.svg)](https://github.com/bluesentinelsec/prsr/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-0A7A0A)](https://bluesentinelsec.github.io/prsr/)
[![License: GPL v2](https://img.shields.io/badge/license-GPL--2.0-blue.svg)](LICENSE)

**Docs:** [https://bluesentinelsec.github.io/prsr/](https://bluesentinelsec.github.io/prsr/)

## Why

AI can open a pull request on your behalf. You then review the GitHub diff in the browser, leave line comments, and have AI apply them.

That works, except GitHub shows those comments as you talking to yourself. `prsr` is the same workflow with a local text file instead of the GitHub comment UI.

## Requirements

| | |
|--|--|
| **Python** | 3.8 or newer |
| **GitHub CLI** | [`gh`](https://cli.github.com/) on `PATH`, already authenticated (`gh auth login`) |

`prsr` does not store tokens. It runs `gh` as a subprocess and lets `gh` handle GitHub authentication. Local `--diff` mode does not need `gh`.

## Install

1.0 is installed from this GitHub repository with pip. PyPI is not used.

Latest `main`:

```bash
pip install git+https://github.com/bluesentinelsec/prsr.git
```

Pin a release tag (recommended):

```bash
pip install git+https://github.com/bluesentinelsec/prsr.git@v1.0.0
```

From a local clone:

```bash
git clone https://github.com/bluesentinelsec/prsr.git
cd prsr
pip install .
```

## Usage

```bash
# numbered diff for a pull request (stdout)
prsr --pr 1234

# write to a file
prsr --pr 1234 -o review.diff

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

Also available: `--verbose` / `-v`, `--version`, `--color auto|always|never`.

On a **terminal**, `--color auto` uses the same colors as Vim's default
`ft=diff` syntax. For a **file you will open in Vim**, skip `--color`. Each
change line starts with `+` or `-`, so Vim's built-in diff syntax colors it
with no plugin:

```bash
prsr --pr 1234 -o review.diff
vim review.diff
```

Full CLI, library API, and review workflow: [the documentation](https://bluesentinelsec.github.io/prsr/).

## Commenting on the file

Output looks like a unified diff with old/new line numbers after the `+`/`-` marker:

```
# prsr numbered diff | OLD  NEW  CODE | source=pr:1234
diff --git a/hello.py b/hello.py
--- a/hello.py
+++ b/hello.py
@@ -1,4 +1,5 @@
    1    1 def greet():
    2    2     name = "world"
-   3          print("hello")
+        3     print("hello,")
+        4     print(name)
    4    5     return name
```

- **OLD** is GitHub's left (before) line number.
- **NEW** is GitHub's right (after) line number.
- Additions have only NEW. Deletions have only OLD. Context lines have both.

Write review notes on their own lines. Leave the numbered source lines alone so line numbers stay aligned:

```
+        3     print("hello,")
# nit: drop the comma
+        4     print(name)
```

Then point your agent at the file.

## Library API

```python
from prsr import render_pr, render_commit, render_compare, render_diff

text = render_pr("1234")
text = render_commit("abc123")
text = render_compare("main", "feature-branch")
text = render_diff(open("unified.diff").read(), source="file:unified.diff")
```

See [Library](https://bluesentinelsec.github.io/prsr/library/) for the full API.

## Development

```bash
python -m pip install -e ".[dev,docs]"
python -m pytest
python -m ruff check src tests
python -m ruff format src tests
python -m mypy
mkdocs serve
```

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[GNU General Public License v2](LICENSE).
