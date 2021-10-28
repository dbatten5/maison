"""Module to hold various utils."""
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
    """Search for a `pyproject.toml` by traversing up the tree from a path.

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


def find_config(
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
        if file_path and source.endswith("toml"):
            return file_path, toml.load(file_path).get("tool", {}).get(project_name, {})

    return None, {}
