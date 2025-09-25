import pathlib
import tempfile
import textwrap
import typing

import pytest

from maison.readers import pyproject


FileFactory = typing.Callable[[str], pathlib.Path]


@pytest.fixture
def tmp_pyproject_file() -> FileFactory:
    """Helper to create a temporary pyproject file."""

    def _create(content: str) -> pathlib.Path:
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".toml", delete=False
        ) as tmp:
            _ = tmp.write(content)
            tmp.flush()
        return pathlib.Path(tmp.name)

    return _create


class TestParseConfig:
    def test_parse_tool_section_with_values(self, tmp_pyproject_file: FileFactory):
        toml_content = textwrap.dedent("""
            [tool.myapp]
            debug = true
            retries = 3
            url = "https://example.com"
        """)
        path = tmp_pyproject_file(toml_content)

        reader = pyproject.PyprojectReader("myapp")
        result = reader.parse_config(path)

        assert result == {"debug": True, "retries": 3, "url": "https://example.com"}

    def test_returns_empty_dict_if_package_section_missing(
        self, tmp_pyproject_file: FileFactory
    ):
        toml_content = textwrap.dedent("""
            [tool.otherapp]
            enabled = true
        """)
        path = tmp_pyproject_file(toml_content)

        reader = pyproject.PyprojectReader("myapp")
        result = reader.parse_config(path)

        assert result == {}

    def test_returns_empty_dict_if_tool_table_missing(
        self, tmp_pyproject_file: FileFactory
    ):
        toml_content = textwrap.dedent("""
            [build-system]
            requires = ["setuptools"]
        """)
        path = tmp_pyproject_file(toml_content)

        reader = pyproject.PyprojectReader("myapp")
        result = reader.parse_config(path)

        assert result == {}

    def test_parse_nested_values_inside_package(self, tmp_pyproject_file: FileFactory):
        toml_content = textwrap.dedent("""
            [tool.myapp.database]
            host = "localhost"
            port = 5432
        """)
        path = tmp_pyproject_file(toml_content)

        reader = pyproject.PyprojectReader("myapp")
        result = reader.parse_config(path)

        assert result == {"database": {"host": "localhost", "port": 5432}}

    def test_empty_file_returns_empty_dict(self, tmp_pyproject_file: FileFactory):
        path = tmp_pyproject_file("")

        reader = pyproject.PyprojectReader("myapp")
        result = reader.parse_config(path)

        assert result == {}

    def test_missing_file_raises_file_not_found(self, tmp_path: pathlib.Path):
        path = tmp_path / "no_such_pyproject.toml"

        reader = pyproject.PyprojectReader("myapp")
        result = reader.parse_config(path)

        assert result == {}
