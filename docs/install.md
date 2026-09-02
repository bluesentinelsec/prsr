# Install

`prsr` is distributed from this GitHub repository. pip installs from a git URL; PyPI is not used.

## Latest release

The `latest` tag always points at the current release:

```bash
pip install git+https://github.com/bluesentinelsec/prsr.git@latest
```

## Pin a version

Version tags are `vX.Y.Z` and match `src/prsr/_version.py`.

```bash
pip install git+https://github.com/bluesentinelsec/prsr.git@v1.0.0
```

To list tags:

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
