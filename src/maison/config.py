"""Module to hold the `ProjectConfig` class definition."""
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

import toml

from maison.utils import get_pyproject_path


class ProjectConfig:
    """Defines the `ProjectConfig` and provides accessors to get config values."""

    def __init__(self, project_name: str, starting_path: Optional[Path] = None) -> None:
        """Initialize the config.

        Args:
            project_name: the name of the project, to be used to find the right section
                in the config file
            starting_path: an optional starting path to start the search for config
                file
        """
        config_path, config_dict = _find_config(project_name, starting_path)
        self._config_dict: Dict[str, Any] = config_dict or {}
        self.config_path: Optional[Path] = config_path

    def __repr__(self) -> str:
        """Return the __repr__.

        Returns:
            the representation
        """
        return f"{self.__class__.__name__}" f" (config_path={self.config_path})"

    def __str__(self) -> str:
        """Return the __str__.

        Returns:
            the representation
        """
        return self.__repr__()

    def to_dict(self) -> Dict[str, Any]:
        """Return a dict of all the config options.

        Returns:
            a dict of the config options
        """
        return self._config_dict

    def get_option(
        self, option_name: str, default_value: Optional[Any] = None
    ) -> Optional[Any]:
        """Return the value of a config option.

        Args:
            option_name: the config option for which to return the value
            default_value: an option default value if the option isn't set

        Returns:
            The value of the given config option or `None` if it doesn't exist
        """
        return self._config_dict.get(option_name, default_value)


def _find_config(
    project_name: str,
    starting_path: Optional[Path] = None,
) -> Tuple[Optional[Path], Dict[str, Any]]:
    """Find the desired config file.

    Args:
        project_name: the name of the project to be used to find the right section in
            the config file
        starting_path: an optional starting path to start the search

    Returns:
        a tuple of the path to the config file if found, and a dictionary of the config
            values
    """
    pyproject_path: Optional[Path] = get_pyproject_path(starting_path)
    if pyproject_path:
        return pyproject_path, toml.load(pyproject_path).get("tool", {}).get(
            project_name, {}
        )

    return None, {}
