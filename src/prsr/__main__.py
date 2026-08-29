"""Allow ``python -m prsr``."""

import sys

from prsr.cli import main

if __name__ == "__main__":
    sys.exit(main())
