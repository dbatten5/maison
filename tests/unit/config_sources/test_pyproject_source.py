"""Tests for the `PyprojectSource` class."""

from pathlib import Path
from typing import Callable

from maison.config_sources.pyproject_source import PyprojectSource


class TestToDict:
    """Tests for the `to_dict` method."""

    def test_success(self, create_pyproject_toml: Callable[..., Path]) -> None:
        """
        Given an instance of `PyprojectSource` instantiated with
            a valid `pyproject.toml` file,
        When the `to_dict` method is called,
        Then the `pyproject.toml` is loaded
            and the relevant section is converted to a `dict`
        """
        pyproject_path = create_pyproject_toml()

        pyproject_source = PyprojectSource(filepath=pyproject_path, project_name="foo")

        assert pyproject_source.to_dict() == {"bar": "baz"}

    def test_unrecognised_section_name(
        self, create_pyproject_toml: Callable[..., Path]
    ) -> None:
        """
        Given an instance of `PyprojectSource` instantiated with
            a valid `pyproject.toml` file but an unrecognised section name
        When the `to_dict` method is called,
        Then an empty dict is returned
        """
        pyproject_path = create_pyproject_toml(section_name="foo")

        pyproject_source = PyprojectSource(filepath=pyproject_path, project_name="bar")

        assert pyproject_source.to_dict() == {}

    def test_unrecognised_format(self, create_toml: Callable[..., Path]) -> None:
        """
        Given an instance of `PyprojectSource` instantiated with
            an invalid `pyproject.toml`
        When the `to_dict` method is called,
        Then an empty dict is returned
        """
        pyproject_path = create_toml(filename="pyproject.toml", content={"foo": "bar"})

        pyproject_source = PyprojectSource(filepath=pyproject_path, project_name="baz")

        assert pyproject_source.to_dict() == {}
