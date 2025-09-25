import pathlib

import toml

from maison import types


class TomlReader:
    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        try:
            return dict(toml.load(file_path))
        except FileNotFoundError:
            return {}
