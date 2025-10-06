"""A parser for .ini files."""

import configparser
import io
import typing

from maison import typedefs


class IniParser:
    """Responsible for parsing .ini files.

    Implements the `Parser` protocol
    """

    def parse_config(self, file: typing.BinaryIO) -> typedefs.ConfigValues:
        """See the Parser.parse_config method."""
        config = configparser.ConfigParser()
        text_io = io.TextIOWrapper(file, encoding="utf-8")
        try:
            config.read_file(text_io)
        except UnicodeDecodeError:
            return {}
        return {section: dict(config.items(section)) for section in config.sections()}
