# prsr

**prsr** (pronounced "pur-sir") is short for **pull request self-review**.

It prints a GitHub-style unified diff **with old and new line numbers preserved**, as plain text, on your machine. You comment in that file. An agent can read the comments and still know exactly which lines you mean — without you posting review comments on a pull request that GitHub thinks you wrote.

## Why

AI can open a pull request on your behalf. You then review the GitHub diff in the browser, leave line comments, and have AI apply them.

That works, except GitHub shows those comments as you talking to yourself. `prsr` is the same workflow with a local text file instead of the GitHub comment UI.

## Requirements

| | |
|--|--|
| **Python** | 3.8 or newer |
| **GitHub CLI** | [`gh`](https://cli.github.com/) on `PATH`, already authenticated (`gh auth login`) |

`prsr` does not store tokens. It runs `gh` as a subprocess and lets `gh` handle GitHub authentication. Numbering a local file with `--diff` does not need `gh`.

## Next

- [Install](install.md) from this GitHub repository with pip
- [CLI](cli.md) for `--pr`, `--commit`, `--base`/`--head`, and `--diff`
- [Library](library.md) if you want the same rendering from Python
- [Review workflow](workflow.md) for commenting and handing the file to an agent
