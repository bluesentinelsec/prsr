# prsr

<p align="center">
  <img src="docs/assets/prsr.jpg" alt="prsr — pull request self-review" width="560">
</p>

<p align="center">
  <strong>prsr</strong> (pronounced “pur-sir”) — pull request self-review.<br>
  GitHub-style diffs with line numbers, as a local text file.
</p>

<p align="center">
  <a href="https://github.com/bluesentinelsec/prsr/actions/workflows/ci.yml"><img src="https://github.com/bluesentinelsec/prsr/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://bluesentinelsec.github.io/prsr/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-0A7A0A" alt="Docs"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL--2.0-blue.svg" alt="License: GPL v2"></a>
</p>

An agent can open a pull request for you. If you review it on GitHub, those comments show up as you talking to yourself. `prsr` renders the same diff on your machine so you can comment in a file and hand that file to the agent instead.

**Docs:** [https://bluesentinelsec.github.io/prsr/](https://bluesentinelsec.github.io/prsr/)

## Install

Python 3.8+ and [`gh`](https://cli.github.com/) on `PATH` (`gh auth login`). `prsr` does not store tokens; it calls `gh` for GitHub-backed commands. `--diff` does not need `gh`.

Install from this repository. PyPI is not used.

```bash
pip install git+https://github.com/bluesentinelsec/prsr.git
```

Pin a release tag when one exists:

```bash
pip install git+https://github.com/bluesentinelsec/prsr.git@v1.0.0
```

## Quick start

```bash
prsr --pr 1234 -o review.diff
vim review.diff
```

Other sources:

```bash
prsr --commit abc123
prsr --base main --head feature-branch
prsr --repo owner/name --pr 1234
git diff main...HEAD | prsr --diff -
```

`--color auto` colors a terminal. For Vim, skip `--color` and use a `.diff` suffix: hunk lines start with `+` / `-`, so `ft=diff` colors them with no plugin.

## What you comment on

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
# nit: drop the comma
+        4     print(name)
    4    5     return name
```

OLD is GitHub’s left side, NEW is the right. Additions have only NEW; deletions have only OLD. Put notes on their own lines. Leave numbered source lines alone.

## Library

```python
from prsr import render_pr, render_commit, render_compare, render_diff

text = render_pr("1234")
```

See the [library docs](https://bluesentinelsec.github.io/prsr/library/).

## Contributing

```bash
python -m pip install -e ".[dev,docs]"
python -m pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[GNU General Public License v2](LICENSE).
