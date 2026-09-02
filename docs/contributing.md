# Contributing

Development setup, tests, documentation builds, pull requests, and how 1.0 is released from git tags are in the repository's [CONTRIBUTING.md](https://github.com/bluesentinelsec/prsr/blob/main/CONTRIBUTING.md).

Short version:

```bash
python -m pip install -e ".[dev,docs]"
python -m pytest
python -m ruff check src tests
python -m mypy
mkdocs serve
```

Install from git, not PyPI. Default install is `@latest`. Pin a release with `@vX.Y.Z`.
