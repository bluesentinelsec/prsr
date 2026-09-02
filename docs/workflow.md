# Review workflow

Use `prsr` when you want line-accurate review comments in a text file instead of GitHub's pull-request comment UI.

## 1. Render the diff

```bash
prsr --pr 1234 -o review.diff
```

Or from a branch without a PR:

```bash
prsr --base main --head HEAD -o review.diff
```

## 2. Read the numbers

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

Hunk body lines start with `+`, `-`, or a space, so Vim `ft=diff` colors the file with no plugin if you skip `--color`.

## 3. Comment on their own lines

Leave numbered source lines unchanged so the columns stay aligned. Put notes on new lines, typically as `#` comments:

```
+        3     print("hello,")
# nit: drop the comma
+        4     print(name)
```

## 4. Hand the file to an agent

Point the agent at `review.diff` and ask it to apply the comments. The OLD/NEW columns are the same line numbers GitHub would use, so the agent can map a note back to the change without a browser review.

Do not paste the review as comments on a pull request you opened with an agent if you want to avoid GitHub showing you talking to yourself. That is the problem `prsr` exists to skip.
