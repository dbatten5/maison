"""Module to hold the `PyprojectSource` class definition."""
from typing import Any
from typing import Dict

from .toml_source import TomlSource


class PyprojectSource(TomlSource):
    """Class to represent a `pyproject.toml` config source."""

    def to_dict(self) -> Dict[Any, Any]:
        """Convert the project `pyproject.toml` section to a dict.

        Relies on the convention that config related to project `acme` will be located
        under a `[tool.acme]` section in `pyproject.toml`

        Returns:
            a dict of the config options and values
        """
        return dict(self._load_file().get("tool", {}).get(self.project_name, {}))
