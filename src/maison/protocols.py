"""Holds protocols used throughout the package."""

import pathlib
import typing

from maison import types


class Parser(typing.Protocol):
    """Defines the interface for a parser used to parse a config file."""

    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        """Parses a config file.

        Args:
            file_path: the path to the config file

        Returns:
            the parsed config values
        """
        ...
