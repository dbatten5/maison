"""A parser for pyproject.toml files."""

import pathlib

import toml

from maison import types


class PyprojectReader:
    """Responsible for parsing pyproject.toml files.

    Implements the `Parser` protocol
    """

    def __init__(self, package_name: str) -> None:
        """Initialise the pyproject reader.

        Args:
            package_name: the name of the package to look for in file, e.g.
                `acme` part of `[tool.acme]`.
        """
        self._package_name = package_name

    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        """See the Parser.parse_config method."""
        try:
            pyproject_dict = dict(toml.load(file_path))
        except FileNotFoundError:
            return {}
        return dict(pyproject_dict.get("tool", {}).get(self._package_name, {}))
