import configparser
import pathlib

from maison import types


class IniReader:
    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        config = configparser.ConfigParser()
        config.read(file_path)
        return {section: dict(config.items(section)) for section in config.sections()}
