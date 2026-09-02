# Contributing to prsr

Thanks for working on `prsr`. This repository is the 1.0 distribution channel: people install with `pip install git+https://github.com/bluesentinelsec/prsr.git` (optionally pinned to a tag). There is no PyPI upload.

## Setup

Python 3.8 or newer. For GitHub-backed commands, [`gh`](https://cli.github.com/) on `PATH`.

```bash
git clone https://github.com/bluesentinelsec/prsr.git
cd prsr
python -m pip install -e ".[dev,docs]"
```

## Checks

Run the same checks CI runs before you open a pull request:

```bash
python -m pytest
python -m ruff check src tests
python -m ruff format src tests
python -m mypy
```

`ruff format --check src tests` is what CI uses. Format locally with `python -m ruff format src tests`.

Unit tests live under `tests/unit/`. They do not call the GitHub API; `gh` subprocesses are mocked.

## Documentation

User docs are Markdown under `docs/`, built with [MkDocs](https://www.mkdocs.org/) and published to GitHub Pages from `main`.

```bash
mkdocs serve
mkdocs build --strict
```

Edit the files under `docs/` and `mkdocs.yml`. Keep the root `README.md` as the GitHub landing page (install, quick start, links into Pages). Do not duplicate long how-to material in both places; put the full story in `docs/` and a short version in the README.

## Pull requests

1. Branch from `main`.
2. Keep the change scoped. Match the existing module layout (`model` / `logic` / `view` / `gh` / `api` / `cli`).
3. Add or update tests for behavior changes.
4. Update `CHANGELOG.md` under `[Unreleased]`.
5. Open a pull request against `main`. CI must pass.

## Versioning and releases

- Version is defined in `src/prsr/_version.py` and read by the package.
- Changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [SemVer](https://semver.org/).
- A release is a git tag `vX.Y.Z` on `main` whose `X.Y.Z` matches `_version.py`.
- Also move the `latest` tag to that commit so this stays the default install:

  ```bash
  git tag -a vX.Y.Z -m "prsr X.Y.Z"
  git tag -f -a latest -m "Latest release (currently X.Y.Z)" vX.Y.Z
  git push origin vX.Y.Z
  git push origin latest --force
  ```

- Users install with:

  ```bash
  pip install git+https://github.com/bluesentinelsec/prsr.git@latest
  pip install git+https://github.com/bluesentinelsec/prsr.git@vX.Y.Z
  ```

- Do not add a PyPI publish step unless the project later decides to.

## License

Contributions are licensed under the [GNU General Public License v2](LICENSE), the same as the rest of the project.
