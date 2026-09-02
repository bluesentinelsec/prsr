# Install

1.0 is distributed from the GitHub repository. pip installs Python packages from a git URL; PyPI is not used.

## Latest `main`

```bash
pip install git+https://github.com/bluesentinelsec/prsr.git
```

## Pin a release (recommended)

Tags are `vX.Y.Z` and match the package version in `src/prsr/_version.py`.

```bash
pip install git+https://github.com/bluesentinelsec/prsr.git@v1.0.0
```

To see available tags:

```bash
git ls-remote --tags https://github.com/bluesentinelsec/prsr.git
```

## From a local clone

```bash
git clone https://github.com/bluesentinelsec/prsr.git
cd prsr
pip install .
```

Editable install for development:

```bash
pip install -e ".[dev,docs]"
```

## Requirements

- Python 3.8 or newer
- [`gh`](https://cli.github.com/) on `PATH` and authenticated (`gh auth login`), for `--pr`, `--commit`, and `--base`/`--head`
- `--diff` has no GitHub dependency

Confirm the install:

```bash
prsr --version
```
