import io
import textwrap

from maison.parsers import toml


class TestParseConfig:
    def test_parse_single_section(self):
        toml_content = textwrap.dedent("""
            [database]
            host = "localhost"
            port = 5432
        """)
        file = io.BytesIO(toml_content.encode())

        reader = toml.TomlParser()
        result = reader.parse_config(file)

        assert result == {"database": {"host": "localhost", "port": 5432}}

    def test_parse_multiple_sections(self):
        toml_content = textwrap.dedent("""
            [database]
            host = "localhost"
            port = 5432

            [api]
            key = "secret"
            endpoint = "https://example.com"
        """)
        file = io.BytesIO(toml_content.encode())

        reader = toml.TomlParser()
        result = reader.parse_config(file)

        assert result == {
            "database": {"host": "localhost", "port": 5432},
            "api": {"key": "secret", "endpoint": "https://example.com"},
        }

    def test_empty_file_returns_empty_dict(self):
        file = io.BytesIO(b"")
        reader = toml.TomlParser()
        result = reader.parse_config(file)
        assert result == {}

    def test_invalid_toml_returns_empty_dict(self):
        file = io.BytesIO(b"not valid toml!")
        reader = toml.TomlParser()
        result = reader.parse_config(file)
        assert result == {}

    def test_overlapping_keys_in_different_sections(self):
        toml_content = textwrap.dedent("""
            [section1]
            key = "value1"

            [section2]
            key = "value2"
        """)
        file = io.BytesIO(toml_content.encode())

        reader = toml.TomlParser()
        result = reader.parse_config(file)

        assert result == {"section1": {"key": "value1"}, "section2": {"key": "value2"}}

    def test_section_key_returns_subset_of_dict(self):
        toml_content = textwrap.dedent("""
            [tool.section]
            key = "value"
        """)
        file = io.BytesIO(toml_content.encode())

        reader = toml.TomlParser(section_key=("tool", "section"))
        result = reader.parse_config(file)

        assert result == {"key": "value"}

    def test_non_existent_section_key_returns_empty_dict(self):
        toml_content = textwrap.dedent("""
            [tool.section]
            key = "value"
        """)
        file = io.BytesIO(toml_content.encode())

        reader = toml.TomlParser(section_key=("tool", "other_section"))
        result = reader.parse_config(file)

        assert result == {}
