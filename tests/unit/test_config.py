"""Tests for the `Config` classes."""

from pathlib import Path
from typing import Callable

import pytest
from pydantic import BaseModel
from pydantic import ValidationError

from maison.config import UserConfig
from maison.errors import NoSchemaError


class TestUserConfig:
    """Tests for the `UserConfig` class."""

    def test_str(self, create_tmp_file: Callable[..., Path]) -> None:
        pyproject_path = create_tmp_file(filename="pyproject.toml")

        config = UserConfig(package_name="foo", starting_path=pyproject_path)

        assert str(config) == "<class 'UserConfig'>"


class TestDictObject:
    """Tests to ensure that the config is accessible as a dict."""

    def test_valid_pyproject(self, create_pyproject_toml: Callable[..., Path]) -> None:
        """A valid pyproject is parsed to a dict object."""
        pyproject_path = create_pyproject_toml()

        config = UserConfig(package_name="foo", starting_path=pyproject_path)

        assert config.values == {"bar": "baz"}


class TestSourceFiles:
    """Tests for the `source_files` init argument."""

    def test_not_found(self) -> None:
        """Non existent source files are handled."""
        config = UserConfig(package_name="foo", source_files=["foo"])

        assert config.path is None
        assert config.values == {}

    def test_unrecognised_file_extension(
        self,
        create_tmp_file: Callable[..., Path],
    ) -> None:
        """Unrecognised source file extensions are handled."""
        source_path = create_tmp_file(filename="foo.txt")
        config = UserConfig(
            package_name="foo",
            source_files=["foo.txt"],
            starting_path=source_path,
        )

        assert config.path is None
        assert config.values == {}

    def test_single_valid_toml_source(self, create_toml: Callable[..., Path]) -> None:
        """Toml files other than pyproject.toml files are handled."""
        source_path = create_toml(filename="another.toml", content={"bar": "baz"})

        config = UserConfig(
            package_name="foo",
            starting_path=source_path,
            source_files=["another.toml"],
        )

        assert config.path == source_path
        assert config.values["bar"] == "baz"

    def test_multiple_valid_toml_sources(
        self,
        create_pyproject_toml: Callable[..., Path],
        create_toml: Callable[..., Path],
    ) -> None:
        """When there are multiple sources, the first one is used"""
        source_path_1 = create_toml(filename="another.toml", content={"bar": "baz"})

        source_path_2 = create_pyproject_toml(
            section_name="oof", content={"rab": "zab"}
        )

        config = UserConfig(
            package_name="foo",
            starting_path=source_path_2,
            source_files=["another.toml", "pyproject.toml"],
        )

        assert config.discovered_paths == [source_path_1, source_path_2]
        assert config.values["bar"] == "baz"

    def test_absolute_path(self, create_tmp_file: Callable[..., Path]) -> None:
        """Source files can be found using absolute paths"""
        path = create_tmp_file(filename="acme.ini")

        config = UserConfig(
            package_name="foo",
            source_files=[str(path)],
        )

        assert config.discovered_paths == [path]

    def test_absolute_path_not_exist(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """Non existent absolute paths are handled."""
        pyproject_path = create_pyproject_toml()

        config = UserConfig(
            package_name="foo",
            source_files=["~/.config/acme.ini", "pyproject.toml"],
            starting_path=pyproject_path,
        )

        assert config.discovered_paths == [pyproject_path]


class TestIniFiles:
    """Tests for handling x.ini config files."""

    def test_valid_ini_file(self, create_tmp_file: Callable[..., Path]) -> None:
        ini_file = """
[section 1]
option_1 = value_1

[section 2]
option_2 = value_2
        """
        source_path = create_tmp_file(content=ini_file, filename="foo.ini")
        config = UserConfig(
            package_name="foo",
            starting_path=source_path,
            source_files=["foo.ini"],
        )

        assert config.discovered_paths == [source_path]
        assert config.values == {
            "section 1": {"option_1": "value_1"},
            "section 2": {"option_2": "value_2"},
        }


class TestValidation:
    """Tests for schema validation."""

    def test_no_schema(self) -> None:
        config = UserConfig(package_name="acme", starting_path=Path("/"))

        assert config.values == {}

        with pytest.raises(NoSchemaError):
            config.validate()

    def test_one_schema_with_valid_config(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """The config is validated with a given schema."""

        class Schema(BaseModel):
            """Defines schema."""

            bar: str

        pyproject_path = create_pyproject_toml()
        config = UserConfig(
            package_name="foo",
            starting_path=pyproject_path,
            schema=Schema,
        )

        config.validate()

        assert config.values["bar"] == "baz"

    def test_one_schema_injected_at_validation(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """Schemas supplied as an argument are used"""

        class Schema(BaseModel):
            """Defines schema."""

            bar: str

        pyproject_path = create_pyproject_toml()
        config = UserConfig(
            package_name="foo",
            starting_path=pyproject_path,
        )

        config.validate(schema=Schema)

        assert config.values["bar"] == "baz"

    def test_use_schema_values(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """Config values can be cast to the validated values."""

        class Schema(BaseModel, coerce_numbers_to_str=True):
            """Defines schema."""

            bar: str
            other: str = "hello"

        pyproject_path = create_pyproject_toml(content={"bar": 1})
        config = UserConfig(
            package_name="foo",
            starting_path=pyproject_path,
            schema=Schema,
        )

        config.validate()

        assert config.values["bar"] == "1"
        assert config.values["other"] == "hello"

    def test_not_use_schema_values(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """If `use_schema_values` is set to False then don't use validated values."""

        class Schema(BaseModel, coerce_numbers_to_str=True):
            """Defines schema."""

            bar: str
            other: str = "hello"

        pyproject_path = create_pyproject_toml(content={"bar": 1})
        config = UserConfig(
            package_name="foo",
            starting_path=pyproject_path,
            schema=Schema,
        )

        config.validate(use_schema_values=False)

        assert config.values["bar"] == 1
        assert "other" not in config.values

    def test_schema_override(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """Schemas given as an argument are preferred"""

        class InitSchema(BaseModel):
            """Defines schema for 1."""

            bar: str = "schema_1"

        class ArgumentSchema(BaseModel):
            """Defines schema for 2."""

            bar: str = "schema_2"

        pyproject_path = create_pyproject_toml(content={"baz": "baz"})
        config = UserConfig(
            package_name="foo",
            starting_path=pyproject_path,
            schema=InitSchema,
        )

        config.validate(schema=ArgumentSchema)

        assert config.values["bar"] == "schema_2"

    def test_invalid_configuration(
        self,
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """Validation errors are raised when config fails validation."""

        class Schema(BaseModel):
            """Defines schema."""

            bar: str

        pyproject_path = create_pyproject_toml(content={"baz": "baz"})
        config = UserConfig(
            package_name="foo",
            starting_path=pyproject_path,
            schema=Schema,
        )

        with pytest.raises(ValidationError):
            config.validate()

    def test_setter(self) -> None:
        """Schemas can be set using the setter."""

        class Schema(BaseModel):
            """Defines schema."""

        config = UserConfig(package_name="foo")

        assert config.schema is None

        config.schema = Schema

        assert config.schema is Schema


class TestMergeConfig:
    """Tests for the merging of multiple config sources."""

    def test_no_overwrites(
        self,
        create_toml: Callable[..., Path],
        create_tmp_file: Callable[..., Path],
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """Configs without overlapping values are merged."""
        config_1_path = create_toml(filename="config.toml", content={"option_1": True})
        ini_file = """
[foo]
option_2 = true
        """
        config_2_path = create_tmp_file(filename="config.ini", content=ini_file)
        pyproject_path = create_pyproject_toml(content={"option_3": True})

        config = UserConfig(
            package_name="foo",
            source_files=[str(config_1_path), str(config_2_path), "pyproject.toml"],
            starting_path=pyproject_path,
            merge_configs=True,
        )

        assert config.path == [config_1_path, config_2_path, pyproject_path]
        assert config.values == {
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
        """Configs with overlapping values are merged."""
        config_1_path = create_toml(
            filename="config_1.toml", content={"option": "config_1"}
        )
        config_2_path = create_toml(
            filename="config_2.toml", content={"option": "config_2"}
        )
        pyproject_path = create_pyproject_toml(content={"option": "config_3"})

        config = UserConfig(
            package_name="foo",
            source_files=[str(config_1_path), str(config_2_path), "pyproject.toml"],
            starting_path=pyproject_path,
            merge_configs=True,
        )

        assert config.values == {
            "option": "config_3",
        }

    def test_nested(
        self,
        create_toml: Callable[..., Path],
        create_pyproject_toml: Callable[..., Path],
    ) -> None:
        """Configs with nested overlapping values are deep merged."""
        config_1_path = create_toml(
            filename="config_1.toml", content={"option": {"nested_1": "config_1"}}
        )
        config_2_path = create_toml(
            filename="config_2.toml", content={"option": {"nested_2": "config_2"}}
        )
        pyproject_path = create_pyproject_toml(
            content={"option": {"nested_2": "config_3"}}
        )

        config = UserConfig(
            package_name="foo",
            source_files=[str(config_1_path), str(config_2_path), "pyproject.toml"],
            starting_path=pyproject_path,
            merge_configs=True,
        )

        assert config.values == {
            "option": {"nested_1": "config_1", "nested_2": "config_3"},
        }
