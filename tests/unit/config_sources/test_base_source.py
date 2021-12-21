"""Tests for the `BaseSource` class."""
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict

from maison.config_sources.base_source import BaseSource


class ConcreteSource(BaseSource):
    """Concretion of `BaseSource` for testing purposes"""

    def to_dict(self) -> Dict[Any, Any]:
        """Return a dict."""
        return {}


class TestFilename:
    """Tests for the `filename` property."""

    def test_success(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given a file,
        When an extension of `BaseSource` is created with the file,
        Then the filename can be retrieved
        """
        path_to_file = create_tmp_file(filename="file.txt")

        source = ConcreteSource(filepath=path_to_file, project_name="acme")

        assert source.filename == "file.txt"
