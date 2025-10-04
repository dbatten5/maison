"""Store the classes and fixtures used throughout the tests."""

from pathlib import Path
from typing import Any
from typing import Callable
from typing import Optional

import pytest


@pytest.fixture(name="create_tmp_file")
def create_tmp_file_fixture(tmp_path: Path) -> Callable[..., Path]:
    """Fixture for creating a temporary file."""

    def _create_tmp_file(content: str = "", filename: str = "file.txt") -> Path:
        tmp_file = tmp_path / filename
        tmp_file.write_text(content)
        return tmp_file

    return _create_tmp_file


@pytest.fixture
def create_pyproject_toml(create_toml: Callable[..., Path]) -> Callable[..., Path]:
    """Fixture for creating a `pyproject.toml`."""

    def _create_pyproject_toml(
        section_name: str = "foo",
        content: Optional[dict[str, Any]] = None,
        filename: str = "pyproject.toml",
    ) -> Path:
        content = content or {"bar": "baz"}
        config_dict = {"tool": {section_name: content}}
        return create_toml(filename=filename, content=config_dict)

    return _create_pyproject_toml
