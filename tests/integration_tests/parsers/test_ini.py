import pathlib
import tempfile
import textwrap
import typing

import pytest

from maison.parsers import ini


FileFactory = typing.Callable[[str], pathlib.Path]


@pytest.fixture
def tmp_ini_file() -> FileFactory:
    """Helper to create a temporary ini file."""

    def _create(content: str) -> pathlib.Path:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".ini", delete=False) as tmp:
            _ = tmp.write(content)
            tmp.flush()
        return pathlib.Path(tmp.name)

    return _create


class TestParseConfig:
    def test_parse_single_section(self, tmp_ini_file: FileFactory):
        ini_content = textwrap.dedent("""
            [database]
            host = localhost
            port = 5432
        """)
        path = tmp_ini_file(ini_content)

        reader = ini.IniParser()
        result = reader.parse_config(path)

        assert result == {"database": {"host": "localhost", "port": "5432"}}

    def test_parse_multiple_sections(self, tmp_ini_file: FileFactory):
        ini_content = textwrap.dedent("""
            [database]
            host = localhost
            port = 5432

            [api]
            key = secret
            endpoint = https://example.com
        """)
        path = tmp_ini_file(ini_content)

        reader = ini.IniParser()
        result = reader.parse_config(path)

        assert result == {
            "database": {"host": "localhost", "port": "5432"},
            "api": {"key": "secret", "endpoint": "https://example.com"},
        }

    def test_empty_file_returns_empty_dict(self, tmp_ini_file: FileFactory):
        path = tmp_ini_file("")

        reader = ini.IniParser()
        result = reader.parse_config(path)

        assert result == {}

    def test_missing_file_returns_empty_dict(self, tmp_path: pathlib.Path):
        path = tmp_path / "nonexistent.ini"

        reader = ini.IniParser()
        result = reader.parse_config(path)

        assert result == {}

    def test_overlapping_keys_in_different_sections(self, tmp_ini_file: FileFactory):
        ini_content = textwrap.dedent("""
            [section1]
            key = value1

            [section2]
            key = value2
        """)
        path = tmp_ini_file(ini_content)

        reader = ini.IniParser()
        result = reader.parse_config(path)

        assert result == {"section1": {"key": "value1"}, "section2": {"key": "value2"}}
