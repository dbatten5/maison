"""Tests for the `IniSource` class."""

from pathlib import Path
from typing import Callable

from maison.config_sources.ini_source import IniSource


class TestToDict:
    """Tests for the `to_dict` method."""

    def test_success(self, create_tmp_file: Callable[..., Path]) -> None:
        """A `.ini` file is converted to a `dict`"""
        ini_file = """
[section 1]
option_1 = value_1

[section 2]
option_2 = value_2
        """
        ini_path = create_tmp_file(content=ini_file, filename="foo.ini")

        toml_source = IniSource(filepath=ini_path, package_name="acme")

        assert toml_source.to_dict() == {
            "section 1": {"option_1": "value_1"},
            "section 2": {"option_2": "value_2"},
        }

    def test_empty_file(self, create_tmp_file: Callable[..., Path]) -> None:
        """Empty `.ini` returns an empty dict"""
        ini_path = create_tmp_file(filename="foo.ini")

        toml_source = IniSource(filepath=ini_path, package_name="acme")

        assert toml_source.to_dict() == {}
