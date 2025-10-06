import io
import pathlib
import typing

import pytest

from maison import config_parser
from maison import errors
from maison import typedefs


class FakePyprojectParser:
    def parse_config(self, file: typing.BinaryIO) -> typedefs.ConfigValues:
        return {"config": "pyproject"}


class FakeTomlParser:
    def parse_config(self, file: typing.BinaryIO) -> typedefs.ConfigValues:
        return {"config": "toml"}


class TestParsesConfig:
    def setup_method(self):
        self.parser = config_parser.ConfigParser()

    def test_uses_parser_by_file_path_and_stem(self):
        self.parser.register_parser(
            suffix=".toml", parser=FakePyprojectParser(), stem="pyproject"
        )

        values = self.parser.parse_config(
            file_path=pathlib.Path("path/to/pyproject.toml"),
            file=io.BytesIO(b"file"),
        )

        assert values == {"config": "pyproject"}

    def test_falls_back_to_suffix(self):
        self.parser.register_parser(
            suffix=".toml", parser=FakePyprojectParser(), stem="pyproject"
        )
        self.parser.register_parser(suffix=".toml", parser=FakeTomlParser())

        values = self.parser.parse_config(
            pathlib.Path("path/to/.acme.toml"),
            file=io.BytesIO(b"file"),
        )

        assert values == {"config": "toml"}

    def test_raises_error_if_no_parser_available(self):
        with pytest.raises(errors.UnsupportedConfigError):
            _ = self.parser.parse_config(
                pathlib.Path("path/to/.acme.toml"),
                file=io.BytesIO(b"file"),
            )
