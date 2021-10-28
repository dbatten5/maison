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


class TestSourceFiles:
    """Tests for the `source_files` init argument."""

    def test_not_found(self) -> None:
        """
        Given a source filename which doesn't exist,
        When the `ProjectConfig` is instantiated with the source,
        Then the config dict is empty
        """
        config = ProjectConfig(project_name="foo", source_files=["foo"])

        assert str(config) == "ProjectConfig (config_path=None)"
        assert config.to_dict() == {}

    def test_single_valid_toml_source(
        self, create_tmp_file: Callable[..., Path]
    ) -> None:
        """
        Given a `toml` source file other than `pyproject.toml`,
        When the `ProjectConfig` is instantiated with the source,
        Then the source is retrieved correctly
        """
        config_toml = toml.dumps({"tool": {"foo": {"bar": "baz"}}})
        source_path = create_tmp_file(content=config_toml, filename="another.toml")

        config = ProjectConfig(
            project_name="foo",
            starting_path=source_path,
            source_files=["another.toml"],
        )

        result = config.get_option("bar")

        assert result == "baz"

    def test_multiple_valid_toml_sources(
        self, create_tmp_file: Callable[..., Path]
    ) -> None:
        """
        Given multiple `toml` source files,
        When the `ProjectConfig` is instantiated with the sources,
        Then first source to be found is retrieved correctly
        """
        config_toml_1 = toml.dumps({"tool": {"foo": {"bar": "baz"}}})
        source_path_1 = create_tmp_file(content=config_toml_1, filename="another.toml")

        config_toml_2 = toml.dumps({"tool": {"oof": {"rab": "zab"}}})
        source_path_2 = create_tmp_file(
            content=config_toml_2, filename="pyproject.toml"
        )

        config = ProjectConfig(
            project_name="foo",
            starting_path=source_path_2,
            source_files=["another.toml", "pyproject.toml"],
        )

        result = config.get_option("bar")

        assert str(config) == f"ProjectConfig (config_path={source_path_1})"
        assert result == "baz"


class TestIniFiles:
    """Tests for handling x.ini config files."""

    def test_valid_ini_file(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given a valid .ini file as a source,
        When the `ProjectConfig` is instantiated with the sources,
        Then the .ini file is parsed and the config dict is populated
        """
        ini_file = """
[section 1]
option_1 = value_1

[section 2]
option_2 = value_2
        """
        source_path = create_tmp_file(content=ini_file, filename="foo.ini")
        config = ProjectConfig(
            project_name="foo",
            starting_path=source_path,
            source_files=["foo.ini"],
        )

        assert str(config) == f"ProjectConfig (config_path={source_path})"
        assert config.to_dict() == {
            "section 1": {"option_1": "value_1"},
            "section 2": {"option_2": "value_2"},
        }
