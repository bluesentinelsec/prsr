"""Unified diff samples used by unit tests."""

HELLO_DIFF = """diff --git a/hello.py b/hello.py
index 1111111..2222222 100644
--- a/hello.py
+++ b/hello.py
@@ -1,4 +1,5 @@
 def greet():
     name = "world"
-    print("hello")
+    print("hello,")
+    print(name)
     return name
"""

NEW_FILE_DIFF = """diff --git a/new.py b/new.py
new file mode 100644
index 0000000..aaa1111
--- /dev/null
+++ b/new.py
@@ -0,0 +1,2 @@
+alpha
+beta
"""

DELETED_FILE_DIFF = """diff --git a/old.py b/old.py
deleted file mode 100644
index aaa1111..0000000
--- a/old.py
+++ /dev/null
@@ -1,2 +0,0 @@
-alpha
-beta
"""

BINARY_DIFF = """diff --git a/icon.png b/icon.png
index 1111111..2222222 100644
Binary files a/icon.png and b/icon.png differ
"""

NO_NEWLINE_DIFF = """diff --git a/notes.txt b/notes.txt
index 1111111..2222222 100644
--- a/notes.txt
+++ b/notes.txt
@@ -1 +1 @@
-hello
+hello world
\\ No newline at end of file
"""

MULTI_FILE_DIFF = """diff --git a/a.txt b/a.txt
index 111..222 100644
--- a/a.txt
+++ b/a.txt
@@ -1 +1,2 @@
 keep
+added
diff --git a/b.txt b/b.txt
index 333..444 100644
--- a/b.txt
+++ b/b.txt
@@ -1,2 +1 @@
 keep
-removed
"""

RENAME_DIFF = """diff --git a/old_name.py b/new_name.py
similarity index 90%
rename from old_name.py
rename to new_name.py
index 111..222 100644
--- a/old_name.py
+++ b/new_name.py
@@ -1,3 +1,3 @@
 first
-second
+second line
 third
"""

OMITTED_COUNTS_DIFF = """diff --git a/one.txt b/one.txt
--- a/one.txt
+++ b/one.txt
@@ -1 +1 @@
-old
+new
"""

TWO_HUNKS_DIFF = """diff --git a/wide.py b/wide.py
--- a/wide.py
+++ b/wide.py
@@ -1,2 +1,2 @@
-alpha
+ALPHA
 beta
@@ -99,2 +99,3 @@
 gamma
-delta
+DELTA
+epsilon
"""
