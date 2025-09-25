import pathlib
import typing

from maison import errors
from maison import types


ParserDictKey = tuple[str, typing.Union[str, None]]


class Parser(typing.Protocol):
    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues: ...


class ConfigReader:
    def __init__(self) -> None:
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
