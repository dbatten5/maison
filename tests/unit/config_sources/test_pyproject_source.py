"""Tests for the `PyprojectSource` class."""

from pathlib import Path
from typing import Callable

from maison.config_sources.pyproject_source import PyprojectSource


class TestToDict:
    """Tests for the `to_dict` method."""

    def test_success(self, create_pyproject_toml: Callable[..., Path]) -> None:
        pyproject_path = create_pyproject_toml()

        pyproject_source = PyprojectSource(filepath=pyproject_path, package_name="foo")

        assert pyproject_source.to_dict() == {"bar": "baz"}

    def test_unrecognised_section_name(
        self, create_pyproject_toml: Callable[..., Path]
    ) -> None:
        """An empty dict is returned if the package name is not found"""
        pyproject_path = create_pyproject_toml(section_name="foo")

        pyproject_source = PyprojectSource(filepath=pyproject_path, package_name="bar")

        assert pyproject_source.to_dict() == {}

    def test_unrecognised_format(self, create_toml: Callable[..., Path]) -> None:
        """An unrecognised format or pyproject.toml returns an empty dict"""
        pyproject_path = create_toml(filename="pyproject.toml", content={"foo": "bar"})

        pyproject_source = PyprojectSource(filepath=pyproject_path, package_name="baz")

        assert pyproject_source.to_dict() == {}
