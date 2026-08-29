# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Color for numbered diffs on a TTY (`--color auto`): same palette as Vim's
  default `ft=diff` syntax (Added green, Removed bright red, file headers
  green, hunk headers brown, index magenta, comments blue). File output is
  plain unless you opt in with `--color` / `--color always`.
- Hunk body lines now start with the unified-diff marker (`+`, `-`, or
  space) so Vim `ft=diff` colors adds/deletes with no plugin and no ANSI.

## [0.1.0] - 2026-08-28

### Added

- Initial release of `prsr` (pull request self-review).
- Numbered unified diffs via `prsr --pr`, `--commit`, `--base`/`--head`, and `--diff`.
- Library API: `render_pr`, `render_commit`, `render_compare`, `render_diff`.
- GitHub CLI (`gh`) used as the only network/auth dependency.
