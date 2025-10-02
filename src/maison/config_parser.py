"""Holds the tools for parsing a config."""

import pathlib
import typing

from maison import errors
from maison import types


ParserDictKey = tuple[str, typing.Union[str, None]]


class Parser(typing.Protocol):
    """Defines the interface for a `Parser` class that's used to parse a config."""

    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        """Parse a config file.

        Args:
            file_path: the path to the config file

        Returns:
            the config values
        """
        ...


class ConfigParser:
    """A utility class used to parse a config."""

    def __init__(self) -> None:
        """Instantiate the class."""
        self._parsers: dict[ParserDictKey, Parser] = {}

    def register_parser(
        self,
        suffix: str,
        parser: Parser,
        stem: typing.Optional[str] = None,
    ) -> None:
        """Register a parser for a file suffix, optionally restricted by filename stem."""
        key = (suffix, stem)
        self._parsers[key] = parser

    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        """See `Parser.parse_config`."""
        key: ParserDictKey

        # First try (suffix, stem)
        key = (file_path.suffix, file_path.stem)
        if key in self._parsers:
            return self._parsers[key].parse_config(file_path)

        # Then fallback to (suffix, None)
        key = (file_path.suffix, None)
        if key in self._parsers:
            return self._parsers[key].parse_config(file_path)

        raise errors.UnsupportedConfigError(f"No parser registered for {file_path}")
