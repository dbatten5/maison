import pathlib

import pytest

from maison import config_reader
from maison import errors
from maison import types


class FakePyprojectParser:
    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        return {"config": "pyproject"}


class FakeTomlParser:
    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        return {"config": "toml"}


class TestParsesConfig:
    def setup_method(self):
        self.reader = config_reader.ConfigReader()

    def test_uses_parser_by_file_path_and_stem(self):
        self.reader.register_parser(
            suffix=".toml", parser=FakePyprojectParser(), stem="pyproject"
        )

        values = self.reader.parse_config(pathlib.Path("path/to/pyproject.toml"))

        assert values == {"config": "pyproject"}

    def test_falls_back_to_suffix(self):
        self.reader.register_parser(
            suffix=".toml", parser=FakePyprojectParser(), stem="pyproject"
        )
        self.reader.register_parser(suffix=".toml", parser=FakeTomlParser())

        values = self.reader.parse_config(pathlib.Path("path/to/.acme.toml"))

        assert values == {"config": "toml"}

    def test_raises_error_if_no_parser_available(self):
        with pytest.raises(errors.UnsupportedConfigError):
            _ = self.reader.parse_config(pathlib.Path("path/to/.acme.toml"))
