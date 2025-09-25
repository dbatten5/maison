import pathlib
import textwrap

import pydantic
import pytest

from maison import config


class TestConfig:
    def test_gets_config_defaults_to_pyproject(self, tmp_path: pathlib.Path):
        fp = tmp_path / "pyproject.toml"
        content = textwrap.dedent("""
            [tool.acme]
            hello = true
        """)
        _ = fp.write_text(content)

        cfg = config.UserConfig(package_name="acme", starting_path=tmp_path)

        assert cfg.values == {"hello": True}
        assert cfg.discovered_paths == [fp]
        assert cfg.path == fp

    def test_merges_configs(self, tmp_path: pathlib.Path):
        pyproject_fp = tmp_path / "pyproject.toml"
        content = textwrap.dedent("""
            [tool.acme]
            hello = true
        """)
        _ = pyproject_fp.write_text(content)

        toml_fp = tmp_path / ".acme.toml"
        content = textwrap.dedent("""
            goodbye = true
        """)
        _ = toml_fp.write_text(content)

        cfg = config.UserConfig(
            package_name="acme",
            source_files=["pyproject.toml", ".acme.toml"],
            starting_path=tmp_path,
            merge_configs=True,
        )

        assert cfg.values == {"hello": True, "goodbye": True}
        assert cfg.discovered_paths == [pyproject_fp, toml_fp]
        assert cfg.path == [pyproject_fp, toml_fp]


class TestValidation:
    def test_validates_config(self, tmp_path: pathlib.Path):
        fp = tmp_path / "pyproject.toml"
        content = textwrap.dedent("""
            [tool.acme]
            foo = "bar"
        """)
        _ = fp.write_text(content)

        class Schema(pydantic.BaseModel):
            foo: int

        cfg = config.UserConfig(
            package_name="acme", starting_path=tmp_path, schema=Schema
        )

        with pytest.raises(pydantic.ValidationError):
            _ = cfg.validate()

    def test_raises_error_if_no_schema(self):
        cfg = config.UserConfig(package_name="acme")

        with pytest.raises(errors.NoSchemaError):
            _ = cfg.validate()
