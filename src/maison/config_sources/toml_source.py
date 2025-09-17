"""Module to hold the `TomlSource` class definition."""

from functools import lru_cache
from typing import Any

import toml

from ..errors import BadTomlError
from .base_source import BaseSource


class TomlSource(BaseSource):
    """Class to represent a `.toml` config source."""

    def to_dict(self) -> dict[Any, Any]:
        """Convert the source config file to a dict.

        Returns:
            a dict of the config options and values
        """
        return self._load_file()

    @lru_cache
    def _load_file(self) -> dict[Any, Any]:
        """Load the `.toml` file.

        Returns:
            the `.toml` source converted to a `dict`

        Raises:
            BadTomlError: If toml cannot be parsed
        """
        try:
            return dict(toml.load(self.filepath))
        except toml.decoder.TomlDecodeError as exc:
            raise BadTomlError(
                f"Error trying to load toml file '{self.filepath}'"
            ) from exc
