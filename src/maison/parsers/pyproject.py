"""A parser for pyproject.toml files."""

from maison.parsers import toml


class PyprojectParser(toml.TomlParser):
    """Responsible for parsing pyproject.toml files.

    Implements the `Parser` protocol
    """

    def __init__(self, tool_name: str) -> None:
        """Initialise the pyproject reader.

        Args:
            tool_name: the name of the package to look for in file, e.g.
                `acme` part of `[tool.acme]`.
        """
        super().__init__(section_key=("tool", tool_name))
