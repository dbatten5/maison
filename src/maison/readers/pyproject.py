import pathlib

import toml

from maison import types


class PyprojectReader:
    def __init__(self, package_name: str) -> None:
        self._package_name = package_name

    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        try:
            pyproject_dict = dict(toml.load(file_path))
        except FileNotFoundError:
            return {}
        return dict(pyproject_dict.get("tool", {}).get(self._package_name, {}))
