"""Tests for the `TomlSource` class."""
from pathlib import Path
from typing import Callable

from maison.config_sources.toml_source import TomlSource


class TestToDict:
    """Tests for the `to_dict` method."""

    def test_success(self, create_toml: Callable[..., Path]) -> None:
        """
        Given an instance of `TomlSource` instantiated with a `.toml` file,
        When the `to_dict` method is called,
        Then the `.toml` is loaded and converted to a `dict`
        """
        toml_path = create_toml(filename="config.toml", content={"foo": "bar"})

        toml_source = TomlSource(filepath=toml_path, project_name="acme")

        assert toml_source.to_dict() == {"foo": "bar"}
