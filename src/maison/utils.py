"""Module to hold various utils."""
import configparser
from functools import lru_cache
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import toml


def path_contains_file(path: Path, filename: str) -> bool:
    """Determine whether a file exists in the given path.

    Args:
        path: the path in which to search for the file
        filename: the name of the file

    Returns:
        A boolean to indicate whether the given file exists in the given path
    """
    return (path / filename).is_file()


def get_file_path(
    filename: str, starting_path: Optional[Path] = None
) -> Optional[Path]:
    """Search for a file by traversing up the tree from a path.

    Args:
        filename: the name of the file to search for
        starting_path: an optional path from which to start searching

    Returns:
        The `Path` to the file if it exists or `None` if it doesn't
    """
    start: Path = starting_path or Path.cwd()

    for path in [start, *start.parents]:
        if path_contains_file(path=path, filename=filename):
            return path / filename

    return None


def _find_config(
    project_name: str,
    source_files: List[str],
    starting_path: Optional[Path] = None,
) -> Tuple[Optional[Path], Dict[str, Any]]:
    """Find the desired config file.

    Args:
        project_name: the name of the project to be used to find the right section in
            the config file
        source_files: a list of source config filenames to look for. The first one found
            will be selected
        starting_path: an optional starting path to start the search

    Returns:
        a tuple of the path to the config file if found, and a dictionary of the config
            values
    """
    for source in source_files:
        file_path: Optional[Path] = get_file_path(
            filename=source,
            starting_path=starting_path,
        )

        if not file_path:
            continue

        if source.endswith("toml"):
            return file_path, _parse_toml(
                file_path=file_path, section_name=project_name
            )

        if source.endswith("ini"):
            return file_path, _parse_ini(file_path=file_path)

    return None, {}


@lru_cache()
def _parse_toml(file_path: Path, section_name: str) -> Dict[str, Any]:
    """Parse a `.toml` file and return the values as a dict.

    Args:
        file_path: the path to the `.toml` file
        section_name: the section header name, to be used as `[tool.{section_name}]`

    Returns:
        a dict of the values
    """
    return dict(toml.load(file_path).get("tool", {}).get(section_name, {}))


@lru_cache()
def _parse_ini(file_path: Path) -> Dict[str, Any]:
    """Parse a `.ini` file and return the values as a dict.

    Args:
        file_path: the path to the `.ini` file

    Returns:
        a dict of the values
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    return {section: dict(config.items(section)) for section in config.sections()}
