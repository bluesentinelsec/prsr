"""Version and package layout checks."""

from prsr import __version__
from prsr._version import __version__ as file_version


def test_version_is_semver():
    parts = __version__.split(".")
    assert len(parts) == 3
    for part in parts:
        assert part.isdigit()


def test_public_version_matches_file():
    assert __version__ == file_version
    assert __version__ == "0.1.0"
