# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-28

### Added

- Initial release of `prsr` (pull request self-review).
- Numbered unified diffs via `prsr --pr`, `--commit`, `--base`/`--head`, and `--diff`.
- Library API: `render_pr`, `render_commit`, `render_compare`, `render_diff`.
- GitHub CLI (`gh`) used as the only network/auth dependency.
