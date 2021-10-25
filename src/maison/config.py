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
        """Initialize the config."""
        config_path, config_dict = _find_config(project_name, starting_path)
        self._config_dict: Dict[str, Any] = config_dict or {}
        self.config_path: Optional[Path] = config_path

    def get_option(self, option: str, default: Optional[Any] = None) -> Optional[Any]:
        """Return the value of a config option.

        Args:
            option (str): the config option for which to return the value
            default: an option default value if the option isn't set

        Returns:
            The value of the given config option or `None` if it doesn't exist
        """
        return self._config_dict.get(option, default)


def _find_config(
    project_name: str,
    starting_path: Optional[Path] = None,
) -> Tuple[Optional[Path], Dict[str, Any]]:
    pyproject_path: Optional[Path] = get_pyproject_path(starting_path)
    if pyproject_path:
        return pyproject_path, toml.load(pyproject_path).get("tool", {}).get(
            project_name, {}
        )

    return None, {}
