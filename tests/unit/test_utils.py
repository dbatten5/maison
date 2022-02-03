"""Tests for the `utils` module."""
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import mark
from pytest import param
from pytest import raises

from maison.utils import deep_merge
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
        mock_path.return_value.expanduser.return_value.is_absolute.return_value = False

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

    def test_absolute_path(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given an absolute path to an existing file,
        When the `get_file_path` function is invoked with the filename,
        Then the path to the file is returned
        """
        path_to_file = create_tmp_file(filename="file.txt")

        result = get_file_path(filename=str(path_to_file))

        assert result == path_to_file

    def test_absolute_path_not_exist(self) -> None:
        """
        Given an absolute path to an non-existing file,
        When the `get_file_path` function is invoked with the filename,
        Then None is returned
        """
        result = get_file_path(filename="~/xxxx/yyyy/doesnotexist.xyz")

        assert result is None


@mark.parametrize(
    "a,b,expected",
    [
        param(
            {1: 2, 2: 5},
            {1: 3},
            {1: 3, 2: 5},
            id="simple",
        ),
        param(
            {1: {2: 3, 6: 7}, 2: 5},
            {1: {2: 4}},
            {1: {2: 4, 6: 7}, 2: 5},
            id="nested",
        ),
    ],
)
def test_deep_merge(
    a: Dict[Any, Any],
    b: Dict[Any, Any],
    expected: Dict[Any, Any],
) -> None:
    """
    Given two dictionaries `a` and `b`,
    when the `deep_merge` function is invoked with `a` and `b` as arguments,
    Test that the returned value is as expected.
    """
    assert deep_merge(a, b) == expected
    assert a == expected


def test_deep_merge_dict_into_scalar() -> None:
    """
    Given two incompatible dictionaries `a` and `b`,
    when the `deep_merge` function is invoked with `a` and `b` as arguments,
    Test that a RuntimeError is raised.
    """
    a = {1: 2, 2: 5}
    b = {1: {3: 4}}
    with raises(RuntimeError):
        deep_merge(a, b)
