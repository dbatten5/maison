"""Tests for the `TomlSource` class."""

import re
from pathlib import Path
from textwrap import dedent
from typing import Callable

import pytest

from maison.config_sources.toml_source import TomlSource
from maison.errors import BadTomlError


class TestToDict:
    """Tests for the `to_dict` method."""

    def test_success(self, create_toml: Callable[..., Path]) -> None:
        """A `.toml` is loaded and converted to a `dict`"""
        toml_path = create_toml(filename="config.toml", content={"foo": "bar"})

        toml_source = TomlSource(filepath=toml_path, package_name="acme")

        assert toml_source.to_dict() == {"foo": "bar"}

    def test_toml_decode_error(self, create_toml: Callable[..., Path]) -> None:
        """Toml decoding errors are reported"""
        toml_path = create_toml(filename="config.toml")
        toml_path.write_text(
            dedent(
                """
                "foo" = "bar"
                "foo" = "bar"
                """
            ),
            encoding="utf-8",
        )

        toml_source = TomlSource(filepath=toml_path, package_name="acme")

        error_regex = re.escape(f"Error trying to load toml file '{toml_path!s}'")
        with pytest.raises(BadTomlError, match=error_regex):
            toml_source.to_dict()
