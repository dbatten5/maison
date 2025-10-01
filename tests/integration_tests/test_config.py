import pathlib
import textwrap

import pytest

from maison import config
from maison import errors
from maison import types


class TestUserConfig:
    def test_str(self):
        cfg = config.UserConfig(package_name="acme")

        assert str(cfg) == "<class 'UserConfig'>"

    def test_values(self, tmp_path: pathlib.Path):
        fp = tmp_path / "pyproject.toml"
        content = textwrap.dedent("""
            [tool.acme]
            hello = true
        """)
        _ = fp.write_text(content)

        cfg = config.UserConfig(package_name="acme", starting_path=tmp_path)

        assert cfg.values == {"hello": True}

    def test_values_setter(self):
        cfg = config.UserConfig(package_name="acme")

        cfg.values = {"hello": True}

        assert cfg.values == {"hello": True}

    def test_discovered_paths(self, tmp_path: pathlib.Path):
        fp = tmp_path / "pyproject.toml"
        content = textwrap.dedent("""
            [tool.acme]
            hello = true
        """)
        _ = fp.write_text(content)

        cfg = config.UserConfig(package_name="acme", starting_path=tmp_path)

        assert cfg.discovered_paths == [fp]

    def test_path_no_sources(self, tmp_path: pathlib.Path):
        cfg = config.UserConfig(package_name="acme", starting_path=tmp_path)

        assert cfg.path is None

    def test_path_with_sources(self, tmp_path: pathlib.Path):
        fp = tmp_path / "pyproject.toml"
        content = textwrap.dedent("""
            [tool.acme]
            hello = true
        """)
        _ = fp.write_text(content)

        cfg = config.UserConfig(package_name="acme", starting_path=tmp_path)

        assert cfg.path == fp

    def test_schema(self):
        class Schema:
            def model_dump(self):
                return {}

        cfg = config.UserConfig(package_name="acme", schema=Schema)

        assert cfg.schema == Schema

        class NewSchema:
            def model_dump(self):
                return {}

        cfg.schema = NewSchema
        assert cfg.schema == NewSchema


class TestValidate:
    def test_no_schema(self):
        cfg = config.UserConfig(package_name="acme")

        with pytest.raises(errors.NoSchemaError):
            _ = cfg.validate()

    def test_validaes_config_without_using_schema_values(self, tmp_path: pathlib.Path):
        fp = tmp_path / "pyproject.toml"
        content = textwrap.dedent("""
            [tool.acme]
            hello = true
        """)

        _ = fp.write_text(content)

        class Schema:
            def __init__(self, *args: object, **kwargs: object) -> None:
                pass

            def model_dump(self) -> types.ConfigValues:
                return {"key": "validated"}

        cfg = config.UserConfig(
            package_name="acme", starting_path=tmp_path, schema=Schema
        )

        values = cfg.validate(use_schema_values=False)

        assert values == {"hello": True}

    def test_validaes_config_with_using_schema_values(self, tmp_path: pathlib.Path):
        fp = tmp_path / "pyproject.toml"
        content = textwrap.dedent("""
            [tool.acme]
            hello = true
        """)

        _ = fp.write_text(content)

        class Schema:
            def __init__(self, *args: object, **kwargs: object) -> None:
                pass

            def model_dump(self) -> types.ConfigValues:
                return {"key": "validated"}

        cfg = config.UserConfig(
            package_name="acme", starting_path=tmp_path, schema=Schema
        )

        values = cfg.validate(use_schema_values=True)

        assert values == {"key": "validated"}
