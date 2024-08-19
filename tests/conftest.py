"""Store the classes and fixtures used throughout the tests."""

from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional

import pytest
import toml


@pytest.fixture(name="create_tmp_file")
def create_tmp_file_fixture(tmp_path: Path) -> Callable[..., Path]:
    """Fixture for creating a temporary file."""

    def _create_tmp_file(content: str = "", filename: str = "file.txt") -> Path:
        tmp_file = tmp_path / filename
        tmp_file.write_text(content)
        return tmp_file

    return _create_tmp_file


@pytest.fixture(name="create_toml")
def create_toml_fixture(create_tmp_file: Callable[..., Path]) -> Callable[..., Path]:
    """Fixture for creating a `.toml` file."""

    def _create_toml(
        filename: str,
        content: Optional[Dict[str, Any]] = None,
    ) -> Path:
        content = content or {}
        config_toml = toml.dumps(content)
        return create_tmp_file(content=config_toml, filename=filename)

    return _create_toml


@pytest.fixture()
def create_pyproject_toml(create_toml: Callable[..., Path]) -> Callable[..., Path]:
    """Fixture for creating a `pyproject.toml`."""

    def _create_pyproject_toml(
        section_name: str = "foo",
        content: Optional[Dict[str, Any]] = None,
        filename: str = "pyproject.toml",
    ) -> Path:
        content = content or {"bar": "baz"}
        config_dict = {"tool": {section_name: content}}
        return create_toml(filename=filename, content=config_dict)

    return _create_pyproject_toml
