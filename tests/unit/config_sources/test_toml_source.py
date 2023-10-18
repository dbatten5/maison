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
        """
        Given an instance of `TomlSource` instantiated with a `.toml` file,
        When the `to_dict` method is called,
        Then the `.toml` is loaded and converted to a `dict`
        """
        toml_path = create_toml(filename="config.toml", content={"foo": "bar"})

        toml_source = TomlSource(filepath=toml_path, project_name="acme")

        assert toml_source.to_dict() == {"foo": "bar"}

    def test_toml_decode_error(self, create_toml: Callable[..., Path]) -> None:
        """
        Given a `.toml` file containing duplicate keys, report on the filepath
        of the `.toml` file that triggered the error.
        """
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

        toml_source = TomlSource(filepath=toml_path, project_name="acme")

        error_regex = re.escape(f"Error trying to load toml file '{str(toml_path)}'")
        with pytest.raises(BadTomlError, match=error_regex):
            toml_source.to_dict()
