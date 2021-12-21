"""Tests for the `IniSource` class."""
from pathlib import Path
from typing import Callable

from maison.config_sources.ini_source import IniSource


class TestToDict:
    """Tests for the `to_dict` method."""

    def test_success(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given an instance of `IniSource` instantiated with a `.ini` file,
        When the `to_dict` method is called,
        Then the `.ini` is loaded and converted to a `dict`
        """
        ini_file = """
[section 1]
option_1 = value_1

[section 2]
option_2 = value_2
        """
        ini_path = create_tmp_file(content=ini_file, filename="foo.ini")

        toml_source = IniSource(filepath=ini_path, project_name="acme")

        assert toml_source.to_dict() == {
            "section 1": {"option_1": "value_1"},
            "section 2": {"option_2": "value_2"},
        }

    def test_empty_file(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given an instance of `IniSource` instantiated with an empty `.ini` file,
        When the `to_dict` method is called,
        Then an empty `dict` is returned
        """
        ini_path = create_tmp_file(filename="foo.ini")

        toml_source = IniSource(filepath=ini_path, project_name="acme")

        assert toml_source.to_dict() == {}
