"""Tests for the `Config` classes."""
from pathlib import Path
from typing import Callable

import toml

from maison.config import ProjectConfig


class TestProjectConfig:
    """Tests for the `ProjectConfig`."""

    def test_valid_pyproject(self, create_tmp_file: Callable[..., Path]) -> None:
        """
        Given a valid `pyproject.toml`,
        When the `ProjectConfig` class is instantiated,
        Then a config value can be retrieved
        """
        config_toml = toml.dumps({"tool": {"foo": {"bar": "baz"}}})
        pyproject_path = create_tmp_file(content=config_toml, filename="pyproject.toml")
        autoimport_config = ProjectConfig(
            project_name="foo", starting_path=pyproject_path
        )

        result = autoimport_config.get_option("bar")

        assert result == "baz"

    def test_no_pyproject(self) -> None:
        """
        Given no supplied `pyproject.toml`,
        When the `ProjectConfig` class is instantiated,
        Then the situation is handled gracefully
        """
        autoimport_config = ProjectConfig(project_name="foo", starting_path=Path("/"))

        result = autoimport_config.get_option("bar")

        assert result is None

    def test_default(self) -> None:
        """
        Given a `ProjectConfig` object,
        When a missing option is retrieved with a given default,
        Then the default is returned
        """
        autoimport_config = ProjectConfig(project_name="foo", starting_path=Path("/"))

        result = autoimport_config.get_option("bar", "baz")

        assert result == "baz"

    def test_valid_pyproject_with_no_autoimport_section(
        self, create_tmp_file: Callable[..., Path]
    ) -> None:
        """
        Given a valid `pyproject.toml`,
        When the `ProjectConfig` class is instantiated,
        Then a config value can be retrieved
        """
        config_toml = toml.dumps({"foo": "bar"})
        pyproject_path = create_tmp_file(content=config_toml, filename="pyproject.toml")
        autoimport_config = ProjectConfig(
            project_name="baz", starting_path=pyproject_path
        )

        result = autoimport_config.get_option("foo")

        assert result is None
