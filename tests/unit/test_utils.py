"""Tests for the `utils` module."""
from pathlib import Path
from typing import Callable
from unittest.mock import MagicMock
from unittest.mock import patch

from maison.utils import get_file_path
from maison.utils import path_contains_file


class TestContainsFile:
    """Tests for the `contains_file` function"""

    def test_found(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given a path containing a file,
        When the `path_contains_file` function is invoked with the path and filename,
        Then a `True` is returned
        """
        path = create_tmp_file(filename="file.txt")

        result = path_contains_file(path=path.parent, filename="file.txt")

        assert result is True

    def test_not_found(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given a path not containing a file,
        When the `path_contains_file` function is invoked with the path and filename,
        Then a `False` is returned
        """
        path = create_tmp_file(filename="file.txt")

        result = path_contains_file(path=path.parent, filename="other.txt")

        assert result is False


class TestGetFilePath:
    """Tests for the `get_file_path`"""

    @patch("maison.utils.Path", autospec=True)
    def test_in_current_directory(
        self, mock_path: MagicMock, create_tmp_file: Callable[..., Path]
    ) -> None:
        """
        Given a file in the `cwd`,
        When the `get_file_path` function is invoked without a `starting_path`,
        Then the path to the file is returned
        """
        path_to_file = create_tmp_file(filename="file.txt")
        mock_path.cwd.return_value = path_to_file.parent

        result = get_file_path(filename="file.txt")

        assert result == path_to_file

    def test_in_parent_directory(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given a file in the parent of `cwd`,
        When the `get_file_path` function is invoked,
        Then the path to the file is returned
        """
        path_to_file = create_tmp_file(filename="file.txt")
        sub_dir = path_to_file / "sub"

        result = get_file_path(filename="file.txt", starting_path=sub_dir)

        assert result == path_to_file

    def test_not_found(self) -> None:
        """
        Given no in the `cwd` or parent dirs,
        When the `get_file_path` function is invoked,
        Then `None` is returned
        """
        result = get_file_path(filename="file.txt", starting_path=Path("/nowhere"))

        assert result is None

    def test_with_given_path(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given a file in a path,
        When the `get_file_path` function is invoked with a `starting_path`,
        Then the path to the file is returned
        """
        path_to_file = create_tmp_file(filename="file.txt")

        result = get_file_path(filename="file.txt", starting_path=path_to_file)

        assert result == path_to_file
