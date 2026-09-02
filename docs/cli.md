# CLI

The `prsr` command renders a numbered unified diff to stdout or to a file.

Specify **exactly one** source: `--pr`, `--commit`, `--diff`, or `--base` together with `--head`.

## Pull request

```bash
prsr --pr 1234
prsr --pr 1234 -o review.diff
prsr --pr https://github.com/owner/name/pull/1234
prsr --repo owner/name --pr 1234
```

Uses `gh pr diff`. `--repo` is needed when the current directory is not that GitHub repository.

## Commit

```bash
prsr --commit abc123
prsr --repo owner/name --commit abc123
```

## Compare two refs

```bash
prsr --base main --head feature-branch
prsr --base v1.0.0 --head HEAD
```

`--base` and `--head` must be used together. Refs may be branches, tags, or SHAs.

## Local unified diff

No GitHub call. Useful for `git diff` output or a file you already saved.

```bash
prsr --diff unified.diff
git diff main...HEAD | prsr --diff -
```

## Output and color

| Flag | Meaning |
|------|---------|
| `-o`, `--output FILE` | Write the numbered diff to `FILE` instead of stdout |
| `--color auto` | Default. Color a TTY; files stay plain |
| `--color always` or bare `--color` | ANSI color everywhere, including `-o` files |
| `--color never` | No color |
| `-v`, `--verbose` | Debug logging on stderr |
| `--version` | Print `prsr X.Y.Z` |

`NO_COLOR` in the environment disables auto color.

On a terminal, `--color auto` uses the same palette as Vim's default `ft=diff` syntax: added lines green, deleted lines bright red, file headers green, hunk headers brown, `index` magenta, and `#` comments blue.

For a file you will open in Vim, omit `--color`. Each change line starts with `+` or `-` in column 0, so `:set ft=diff` (or a `.diff` suffix) colors it with no plugin and no ANSI:

```bash
prsr --pr 1234 -o review.diff
vim review.diff
```

`less review.diff` will not color, but the leading `+` / `-` still scans like `git diff`.

## Exit status

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | `prsr` error (missing `gh`, GitHub failure, unreadable file, unparseable diff) |
| 2 | Usage error (argparse) |
