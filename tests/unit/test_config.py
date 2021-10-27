"""Tests for the `Config` classes."""
from pathlib import Path
from typing import Callable

import toml

from maison.config import ProjectConfig


class TestProjectConfig:
    """Tests for the `ProjectConfig` class."""

    def test_repr(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given an instance of `ProjectConfig`,
        When the string representation is retrieved,
        Then a useful representation is returned
        """
        pyproject_path = create_tmp_file(filename="pyproject.toml")

        config = ProjectConfig(project_name="foo", starting_path=pyproject_path)

        assert str(config) == f"ProjectConfig (config_path={pyproject_path})"

    def test_repr_no_config_path(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given an instance of `ProjectConfig` without a `config_path`,
        When the string representation is retrieved,
        Then a useful representation is returned
        """
        pyproject_path = create_tmp_file()

        config = ProjectConfig(project_name="foo", starting_path=pyproject_path)

        assert str(config) == "ProjectConfig (config_path=None)"

    def test_to_dict(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given an instance of `ProjectConfig`,
        When the `to_dict` method is invoked,
        Then a dictionary of all config options is returned
        """
        config_dict = {"tool": {"foo": {"bar": "baz"}}}
        config_toml = toml.dumps(config_dict)
        pyproject_path = create_tmp_file(content=config_toml, filename="pyproject.toml")

        config = ProjectConfig(project_name="foo", starting_path=pyproject_path)

        assert config.to_dict() == config_dict["tool"]["foo"]


class TestGetOption:
    """Tests for the `get_option` method."""

    def test_valid_pyproject(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given a valid `pyproject.toml`,
        When the `ProjectConfig` class is instantiated,
        Then a config value can be retrieved
        """
        config_toml = toml.dumps({"tool": {"foo": {"bar": "baz"}}})
        pyproject_path = create_tmp_file(content=config_toml, filename="pyproject.toml")
        config = ProjectConfig(project_name="foo", starting_path=pyproject_path)

        result = config.get_option("bar")

        assert result == "baz"

    def test_no_pyproject(self) -> None:
        """
        Given no supplied `pyproject.toml`,
        When the `ProjectConfig` class is instantiated,
        Then the situation is handled gracefully
        """
        config = ProjectConfig(project_name="foo", starting_path=Path("/"))

        result = config.get_option("bar")

        assert result is None

    def test_default(self) -> None:
        """
        Given a `ProjectConfig` object,
        When a missing option is retrieved with a given default,
        Then the default is returned
        """
        config = ProjectConfig(project_name="foo", starting_path=Path("/"))

        result = config.get_option("bar", "baz")

        assert result == "baz"

    def test_valid_pyproject_with_no_project_section(
        self, create_tmp_file: Callable[..., Path]
    ) -> None:
        """
        Given a valid `pyproject.toml`,
        When the `ProjectConfig` class is instantiated,
        Then a config value can be retrieved
        """
        config_toml = toml.dumps({"foo": "bar"})
        pyproject_path = create_tmp_file(content=config_toml, filename="pyproject.toml")
        config = ProjectConfig(project_name="baz", starting_path=pyproject_path)

        result = config.get_option("foo")

        assert result is None
