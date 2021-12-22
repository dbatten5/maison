"""Tests for the `Config` classes."""
from pathlib import Path
from typing import Callable

import pytest
from pydantic import ValidationError

from maison.config import ProjectConfig
from maison.errors import NoSchemaError
from maison.schema import ConfigSchema


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

        assert str(config) == "<class 'ProjectConfig'>"

    def test_to_dict(self, create_pyproject_toml: Callable[..., Path]) -> None:
        """
        Given an instance of `ProjectConfig`,
        When the `to_dict` method is invoked,
        Then a dictionary of all config options is returned
        """
        pyproject_path = create_pyproject_toml()

        config = ProjectConfig(project_name="foo", starting_path=pyproject_path)

        assert config.to_dict() == {"bar": "baz"}


class TestGetOption:
    """Tests for the `get_option` method."""

    def test_valid_pyproject(self, create_pyproject_toml: Callable[..., Path]) -> None:
        """
        Given a valid `pyproject.toml`,
        When the `ProjectConfig` class is instantiated,
        Then a config value can be retrieved
        """
        pyproject_path = create_pyproject_toml()
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
        self, create_toml: Callable[..., Path]
    ) -> None:
        """
        Given a valid `pyproject.toml` without a [tool.{project_name}] section,
        When the `ProjectConfig` class is instantiated,
        Then a config value can be retrieved
        """
        pyproject_path = create_toml(filename="pyproject.toml", content={"foo": "bar"})
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

        assert config.config_path is None
        assert config.to_dict() == {}

    def test_unrecognised_file_extension(
        self,
        create_tmp_file: Callable[..., Path],
    ) -> None:
        """
        Given a source with a file extension that isn't recognised,
        When the `ProjectConfig` is instantiated with the source,
        Then the config dict is empty
        """
        source_path = create_tmp_file(filename="foo.txt")
        config = ProjectConfig(
            project_name="foo",
            source_files=["foo.txt"],
            starting_path=source_path,
        )

        assert config.config_paths == []
        assert config.to_dict() == {}

    def test_single_valid_toml_source(self, create_toml: Callable[..., Path]) -> None:
        """
        Given a `toml` source file other than `pyproject.toml`,
        When the `ProjectConfig` is instantiated with the source,
        Then the source is retrieved correctly
        """
        source_path = create_toml(filename="another.toml", content={"bar": "baz"})

        config = ProjectConfig(
            project_name="foo",
            starting_path=source_path,
            source_files=["another.toml"],
        )

        result = config.get_option("bar")

        assert config.config_path == source_path
        assert result == "baz"

    def test_multiple_valid_toml_sources(
        self,
        create_pyproject_toml: Callable[..., Path],
        create_toml: Callable[..., Path],
    ) -> None:
        """
        Given multiple `toml` source files,
        When the `ProjectConfig` is instantiated with the sources,
        Then first source to be found is retrieved correctly
        """
        source_path_1 = create_toml(filename="another.toml", content={"bar": "baz"})

        source_path_2 = create_pyproject_toml(
            section_name="oof", content={"rab": "zab"}
        )

        config = ProjectConfig(
            project_name="foo",
            starting_path=source_path_2,
            source_files=["another.toml", "pyproject.toml"],
        )

        result = config.get_option("bar")

        assert config.config_paths == [source_path_1, source_path_2]
        assert result == "baz"

    def test_absolute_path(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given a source file with an absolute path to an existing config,
        When the `ProjectConfig` is instantiated with the source,
        Then the source is successfully retrieved
        """
        path = create_tmp_file(filename="acme.ini")

        config = ProjectConfig(
            project_name="foo",
            source_files=[str(path)],
        )

        assert config.config_paths == [path]

    def test_absolute_path_not_exist(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """
        Given a source file with an absolute path to an non-existing config,
        When the `ProjectConfig` is instantiated with the source,
        Then the missing source is ignored
        """
        pyproject_path = create_pyproject_toml()

        config = ProjectConfig(
            project_name="foo",
            source_files=["~/.config/acme.ini", "pyproject.toml"],
            starting_path=pyproject_path,
        )

        assert config.config_paths == [pyproject_path]


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

        assert config.config_paths == [source_path]
        assert config.to_dict() == {
            "section 1": {"option_1": "value_1"},
            "section 2": {"option_2": "value_2"},
        }


class TestValidation:
    """Tests for schema validation."""

    def test_no_schema(self) -> None:
        """
        Given an instance of `ProjectConfig` with no schema,
        When the `validate` method is called,
        Then a `NoSchemaError` is raised
        """
        config = ProjectConfig(project_name="acme", starting_path=Path("/"))

        assert config.to_dict() == {}

        with pytest.raises(NoSchemaError):
            config.validate()

    def test_one_schema_with_valid_config(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """
        Given an instance of `ProjectConfig` with a given schema,
        When the `validate` method is called,
        Then the configuration is validated
        """

        class Schema(ConfigSchema):
            """Defines schema."""

            bar: str

        pyproject_path = create_pyproject_toml()
        config = ProjectConfig(
            project_name="foo",
            starting_path=pyproject_path,
            config_schema=Schema,
        )

        config.validate()

        assert config.get_option("bar") == "baz"

    def test_one_schema_injected_at_validation(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """
        Given an instance of `ProjectConfig` with a given schema,
        When the `validate` method is called,
        Then the configuration is validated
        """

        class Schema(ConfigSchema):
            """Defines schema."""

            bar: str

        pyproject_path = create_pyproject_toml()
        config = ProjectConfig(
            project_name="foo",
            starting_path=pyproject_path,
        )

        config.validate(config_schema=Schema)

        assert config.get_option("bar") == "baz"

    def test_use_schema_values(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """
        Given an instance of `ProjectConfig` with a given schema,
        When the `validate` method is called,
        Then the configuration is validated and values are cast to those in the schema
            and default values are used
        """

        class Schema(ConfigSchema):
            """Defines schema."""

            bar: str
            other: str = "hello"

        pyproject_path = create_pyproject_toml(content={"bar": 1})
        config = ProjectConfig(
            project_name="foo",
            starting_path=pyproject_path,
            config_schema=Schema,
        )

        config.validate()

        assert config.get_option("bar") == "1"
        assert config.get_option("other") == "hello"

    def test_not_use_schema_values(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """
        Given an instance of `ProjectConfig` with a given schema,
        When the `validate` method is called with `use_schema_values` set to `False`,
        Then the configuration is validated but values remain as in the config
        """

        class Schema(ConfigSchema):
            """Defines schema."""

            bar: str
            other: str = "hello"

        pyproject_path = create_pyproject_toml(content={"bar": 1})
        config = ProjectConfig(
            project_name="foo",
            starting_path=pyproject_path,
            config_schema=Schema,
        )

        config.validate(use_schema_values=False)

        assert config.get_option("bar") == 1
        assert config.get_option("other") is None

    def test_schema_override(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """
        Given an instance of `ProjectConfig` with a given schema,
        When the `validate` method is called with a new schema,
        Then the new schema is used
        """

        class Schema1(ConfigSchema):
            """Defines schema for 1."""

            bar: str = "schema_1"

        class Schema2(ConfigSchema):
            """Defines schema for 2."""

            bar: str = "schema_2"

        pyproject_path = create_pyproject_toml(content={"baz": "baz"})
        config = ProjectConfig(
            project_name="foo",
            starting_path=pyproject_path,
            config_schema=Schema1,
        )

        config.validate(config_schema=Schema2)

        assert config.get_option("bar") == "schema_2"

    def test_invalid_configuration(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """
        Given a configuration which doesn't conform to the schema,
        When the `validate` method is called,
        Then an error is raised
        """

        class Schema(ConfigSchema):
            """Defines schema."""

            bar: str

        pyproject_path = create_pyproject_toml(content={"baz": "baz"})
        config = ProjectConfig(
            project_name="foo",
            starting_path=pyproject_path,
            config_schema=Schema,
        )

        with pytest.raises(ValidationError):
            config.validate()

    def test_setter(self) -> None:
        """
        Given an instance of `ProjectConfig`,
        When the `config_schema` is set,
        Then the `config_schema` can be retrieved
        """

        class Schema(ConfigSchema):
            """Defines schema."""

        config = ProjectConfig(project_name="foo")

        assert config.config_schema is None

        config.config_schema = Schema

        assert config.config_schema is Schema


class TestMergeConfig:
    """Tests for the merging of multiple config sources."""

    def test_no_overwrites(
        self,
        create_toml: Callable[..., Path],
        create_tmp_file: Callable[..., Path],
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """
        Given multiple existing config sources with no overlapping options,
        When the `merge_configs` boolean is set to `True`,
        Then the configs are merged
        """
        config_1_path = create_toml(filename="config.toml", content={"option_1": True})
        ini_file = """
[foo]
option_2 = true
        """
        config_2_path = create_tmp_file(filename="config.ini", content=ini_file)
        pyproject_path = create_pyproject_toml(content={"option_3": True})

        config = ProjectConfig(
            project_name="foo",
            source_files=[str(config_1_path), str(config_2_path), "pyproject.toml"],
            starting_path=pyproject_path,
            merge_configs=True,
        )

        assert config.config_path == [config_1_path, config_2_path, pyproject_path]
        assert config.to_dict() == {
            "option_1": True,
            "foo": {
                "option_2": "true",
            },
            "option_3": True,
        }

    def test_overwrites(
        self,
        create_toml: Callable[..., Path],
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """
        Given multiple existing config sources with overlapping options,
        When the `merge_configs` boolean is set to `True`,
        Then the configs are merged from right to left
        """
        config_1_path = create_toml(
            filename="config_1.toml", content={"option": "config_1"}
        )
        config_2_path = create_toml(
            filename="config_2.toml", content={"option": "config_2"}
        )
        pyproject_path = create_pyproject_toml(content={"option": "config_3"})

        config = ProjectConfig(
            project_name="foo",
            source_files=[str(config_1_path), str(config_2_path), "pyproject.toml"],
            starting_path=pyproject_path,
            merge_configs=True,
        )

        assert config.to_dict() == {
            "option": "config_3",
        }
