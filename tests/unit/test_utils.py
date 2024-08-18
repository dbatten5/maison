"""Tests for the `utils` module."""

from pathlib import Path
from typing import Callable
from typing import Dict
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from maison.utils import deep_merge
from maison.utils import get_file_path
from maison.utils import path_contains_file


class TestContainsFile:
    """Tests for the `contains_file` function"""

    def test_found(self, create_tmp_file: Callable[..., Path]) -> None:
        """Return `True` if the path contains the file"""
        path = create_tmp_file(filename="file.txt")

        result = path_contains_file(path=path.parent, filename="file.txt")

        assert result is True

    def test_not_found(self, create_tmp_file: Callable[..., Path]) -> None:
        """Return `False` if the path does not contain the file"""
        path = create_tmp_file(filename="file.txt")

        result = path_contains_file(path=path.parent, filename="other.txt")

        assert result is False


class TestGetFilePath:
    """Tests for the `get_file_path`"""

    @patch("maison.utils.Path", autospec=True)
    def test_in_current_directory(
        self, mock_path: MagicMock, create_tmp_file: Callable[..., Path]
    ) -> None:
        """The path to a file is returned."""
        mock_path.return_value.expanduser.return_value.is_absolute.return_value = False

        path_to_file = create_tmp_file(filename="file.txt")
        mock_path.cwd.return_value = path_to_file.parent

        result = get_file_path(filename="file.txt")

        assert result == path_to_file

    def test_in_parent_directory(self, create_tmp_file: Callable[..., Path]) -> None:
        """The path to a file in a parent directory is returned."""
        path_to_file = create_tmp_file(filename="file.txt")
        sub_dir = path_to_file / "sub"

        result = get_file_path(filename="file.txt", starting_path=sub_dir)

        assert result == path_to_file

    def test_not_found(self) -> None:
        """If the file isn't found in the tree then return a `None`"""
        result = get_file_path(filename="file.txt", starting_path=Path("/nowhere"))

        assert result is None

    def test_with_given_path(self, create_tmp_file: Callable[..., Path]) -> None:
        """A `starting_path` can be used to initiate the starting search directory"""
        path_to_file = create_tmp_file(filename="file.txt")

        result = get_file_path(filename="file.txt", starting_path=path_to_file)

        assert result == path_to_file

    def test_absolute_path(self, create_tmp_file: Callable[..., Path]) -> None:
        """An absolute path to an existing file is returned"""
        path_to_file = create_tmp_file(filename="file.txt")

        result = get_file_path(filename=str(path_to_file))

        assert result == path_to_file

    def test_absolute_path_not_exist(self) -> None:
        """If the absolute path doesn't exist return a `None`"""
        result = get_file_path(filename="~/xxxx/yyyy/doesnotexist.xyz")

        assert result is None


class TestDeepMerge:
    """Tests for the `deep_merge` function."""

    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            pytest.param(
                {1: 2, 3: 4},
                {3: 5, 6: 7},
                {1: 2, 3: 5, 6: 7},
                id="simple",
            ),
            pytest.param(
                {1: 2, 3: {4: 5, 6: 7}},
                {3: {6: 8, 9: 10}, 11: 12},
                {1: 2, 3: {4: 5, 6: 8, 9: 10}, 11: 12},
                id="nested",
            ),
        ],
    )
    def test_success(
        self,
        a: Dict[int, int],
        b: Dict[int, int],
        expected: Dict[int, int],
    ) -> None:
        assert deep_merge(a, b) == expected
        assert a == expected

    def test_incompatible_dicts(self) -> None:
        """Trying to merge incompatible dicts returns an error"""
        dict_a = {1: 2, 2: 5}
        dict_b = {1: {3: 4}}

        with pytest.raises(RuntimeError):
            deep_merge(dict_a, dict_b)
