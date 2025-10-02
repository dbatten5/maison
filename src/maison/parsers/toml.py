"""A parser for .toml files."""

import pathlib

import toml

from maison import typedefs


class TomlParser:
    """Responsible for parsing .toml files.

    Implements the `Parser` protocol
    """

    def parse_config(self, file_path: pathlib.Path) -> typedefs.ConfigValues:
        """See the Parser.parse_config method."""
        try:
            return dict(toml.load(file_path))
        except (FileNotFoundError, toml.TomlDecodeError):
            return {}
