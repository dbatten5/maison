"""Holds tools for interacting with the disk filesystem."""

import functools
import pathlib
import typing
from collections.abc import Generator


def _path_contains_file(path: pathlib.Path, filename: str) -> bool:
    """Determine whether a file exists in the given path.

    Args:
        path: the path in which to search for the file
        filename: the name of the file

    Returns:
        A boolean to indicate whether the given file exists in the given path
    """
    return (path / filename).is_file()


def _generate_search_paths(
    starting_path: pathlib.Path,
) -> Generator[pathlib.Path, None, None]:
    """Generate paths from a starting path and traversing up the tree.

    Args:
        starting_path: a starting path to start yielding search paths

    Yields:
        a path from the tree
    """
    yield from [starting_path, *starting_path.parents]


class DiskFilesystem:
    """A class to represent the disk filesystem.

    Implements the `Filesystem` protocol.
    """

    @functools.lru_cache
    def get_file_path(
        self, file_name: str, starting_path: typing.Optional[pathlib.Path] = None
    ) -> typing.Optional[pathlib.Path]:
        """See `Filesystem.get_file_path`."""
        filename_path = pathlib.Path(file_name).expanduser()
        if filename_path.is_absolute() and filename_path.is_file():
            return filename_path

        start = starting_path or pathlib.Path.cwd()

        for path in _generate_search_paths(starting_path=start):
            if _path_contains_file(path=path, filename=file_name):
                return path / file_name

        return None

    def open_file(self, path: pathlib.Path) -> typing.BinaryIO:
        """See `Filesystem.open_file`."""
        return path.open(mode="rb")
