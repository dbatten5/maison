"""Module to hold the `IniSource` class definition."""
from configparser import ConfigParser
from functools import lru_cache
from typing import Any
from typing import Dict

from .base_source import BaseSource


class IniSource(BaseSource):
    """Class to represent a `.ini` config source."""

    def to_dict(self) -> Dict[Any, Any]:
        """Convert the source config file to a dict.

        Returns:
            a dict of the config options and values
        """
        config = self._load_file()
        return {section: dict(config.items(section)) for section in config.sections()}

    @lru_cache()
    def _load_file(self) -> ConfigParser:
        """Load the `.ini` file.

        Returns:
            a `ConfigParser` object with the `.ini` source read into it
        """
        config = ConfigParser()
        config.read(self.filepath)
        return config
