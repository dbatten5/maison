"""Module to hold the `TomlSource` class definition."""
from functools import lru_cache
from typing import Any
from typing import Dict

import toml

from .base_source import BaseSource


class TomlSource(BaseSource):
    """Class to represent a `.toml` config source."""

    def to_dict(self) -> Dict[Any, Any]:
        """Convert the source config file to a dict.

        Returns:
            a dict of the config options and values
        """
        return self._load_file()

    @lru_cache()
    def _load_file(self) -> Dict[Any, Any]:
        """Load the `.toml` file.

        Returns:
            the `.toml` source converted to a `dict`
        """
        return dict(toml.load(self.filepath))