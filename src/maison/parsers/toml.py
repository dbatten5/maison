"""A parser for .toml files."""

import sys


if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import typing

from maison import typedefs


class TomlParser:
    """Responsible for parsing .toml files.

    Implements the `Parser` protocol
    """

    def __init__(self, section_key: typing.Optional[tuple[str, ...]] = None) -> None:
        """Instantiate the class.

        Args:
            section_key: an optional toml section key/identifier to search for
                within the toml. For example if the toml file contains:

                [tool.my_section]
                my_value = true

                then setting `section_key=("tool", "my_section")` will return
                `{"my_value": True}` as the config values.

        """
        self.section_key = section_key or ()

    def parse_config(self, file: typing.BinaryIO) -> typedefs.ConfigValues:
        """See the Parser.parse_config method."""
        try:
            values = dict(tomllib.load(file))
        except tomllib.TOMLDecodeError:
            return {}

        current = values
        for key in self.section_key:
            if key in current and isinstance(current[key], dict):
                current = current[key]
            else:
                return {}

        return current
