"""A parser for .ini files."""

import configparser
import pathlib

from maison import types


class IniParser:
    """Responsible for parsing .ini files.

    Implements the `Parser` protocol
    """

    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        """See the Parser.parse_config method."""
        config = configparser.ConfigParser()
        _ = config.read(file_path)
        return {section: dict(config.items(section)) for section in config.sections()}
