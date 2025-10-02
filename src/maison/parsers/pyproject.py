"""A parser for pyproject.toml files."""

import pathlib
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from maison import typedefs


class PyprojectParser:
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

    def parse_config(self, file_path: pathlib.Path) -> typedefs.ConfigValues:
        """See the Parser.parse_config method."""
        try:
            with file_path.open(mode="rb") as fd:
                pyproject_dict = dict(tomllib.load(fd))
        except FileNotFoundError:
            return {}
        return dict(pyproject_dict.get("tool", {}).get(self._package_name, {}))
