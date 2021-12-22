"""Module to hold various utils."""
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional

from maison.config_sources.base_source import BaseSource
from maison.config_sources.ini_source import IniSource
from maison.config_sources.pyproject_source import PyprojectSource
from maison.config_sources.toml_source import TomlSource


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
        filename: the name of the file or an absolute path to a config to search for
        starting_path: an optional path from which to start searching

    Returns:
        The `Path` to the file if it exists or `None` if it doesn't
    """
    filename_path = Path(filename).expanduser()
    if filename_path.is_absolute() and filename_path.is_file():
        return filename_path

    for path in _generate_search_paths(starting_path=starting_path):
        if path_contains_file(path=path, filename=filename):
            return path / filename

    return None


def _generate_search_paths(
    starting_path: Optional[Path] = None,
) -> Generator[Path, None, None]:
    """Generate paths from either a starting path or `Path.cwd()`.

    Args:
        starting_path: an optional starting path to start yielding search paths

    Yields:
        a path
    """
    starting_path = starting_path or Path.cwd()
    for path in [starting_path, *starting_path.parents]:
        yield path


def _collect_configs(
    project_name: str,
    source_files: List[str],
    starting_path: Optional[Path] = None,
) -> List[BaseSource]:
    """Collect configs and return them in a list.

    Args:
        project_name: the name of the project to be used to find the right section in
            the config file
        source_files: a list of source config filenames to look for. The first one found
            will be selected
        starting_path: an optional starting path to start the search

    Returns:
        a list of the found config sources
    """
    sources: List[BaseSource] = []

    for source in source_files:
        file_path = get_file_path(
            filename=source,
            starting_path=starting_path,
        )

        if not file_path:
            continue

        # Dict[str, Any] to stop mypy complaining:
        # https://github.com/python/mypy/issues/5382#issuecomment-583901369
        source_kwargs: Dict[str, Any] = {
            "filepath": file_path,
            "project_name": project_name,
        }

        if source.endswith("toml"):
            if source.startswith("pyproject"):
                sources.append(PyprojectSource(**source_kwargs))
            else:
                sources.append(TomlSource(**source_kwargs))

        if source.endswith("ini"):
            sources.append(IniSource(**source_kwargs))

    return sources
