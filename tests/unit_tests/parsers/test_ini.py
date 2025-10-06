import io
import textwrap

from maison.parsers import ini


class TestParseConfig:
    def test_parse_single_section(self):
        ini_content = textwrap.dedent("""
            [database]
            host = localhost
            port = 5432
        """)
        file = io.BytesIO(ini_content.encode())

        reader = ini.IniParser()
        result = reader.parse_config(file)

        assert result == {"database": {"host": "localhost", "port": "5432"}}

    def test_parse_multiple_sections(self):
        ini_content = textwrap.dedent("""
            [database]
            host = localhost
            port = 5432

            [api]
            key = secret
            endpoint = https://example.com
        """)
        file = io.BytesIO(ini_content.encode())

        reader = ini.IniParser()
        result = reader.parse_config(file)

        assert result == {
            "database": {"host": "localhost", "port": "5432"},
            "api": {"key": "secret", "endpoint": "https://example.com"},
        }

    def test_empty_file_returns_empty_dict(self):
        file = io.BytesIO()

        reader = ini.IniParser()
        result = reader.parse_config(file)

        assert result == {}

    def test_invalid_bytes_returns_empty_dict(self):
        ini_content = b"\xff\xfe\x00bad ini"
        file = io.BytesIO(ini_content)

        reader = ini.IniParser()
        result = reader.parse_config(file)

        assert result == {}

    def test_overlapping_keys_in_different_sections(self):
        ini_content = textwrap.dedent("""
            [section1]
            key = value1

            [section2]
            key = value2
        """)
        file = io.BytesIO(ini_content.encode())

        reader = ini.IniParser()
        result = reader.parse_config(file)

        assert result == {"section1": {"key": "value1"}, "section2": {"key": "value2"}}
