"""A parser for .toml files."""

import pathlib
import sys


if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from maison import typedefs


class TomlParser:
    """Responsible for parsing .toml files.

    Implements the `Parser` protocol
    """

    def parse_config(self, file_path: pathlib.Path) -> typedefs.ConfigValues:
        """See the Parser.parse_config method."""
        try:
            with file_path.open(mode="rb") as fd:
                return dict(tomllib.load(fd))
        except (FileNotFoundError, tomllib.TOMLDecodeError):
            return {}
