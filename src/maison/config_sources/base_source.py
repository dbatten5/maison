"""Module to hold the `BaseSource` abstract class definition."""
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import Dict


class BaseSource(ABC):
    """Base class from which concrete source abstractions extend."""

    def __init__(self, filepath: Path, project_name: str) -> None:
        """Initialize the object.

        Args:
            filepath: the `Path` to the config file
            project_name: the name of the project, used to pick out the relevant section
                in a `.toml` or `.ini` file
        """
        self.filepath = filepath
        self.project_name = project_name

    def __repr__(self) -> str:
        """Return the __repr__.

        Returns:
            the representation
        """
        return f"<class '{self.__class__.__name__}' path:{self.filepath}>"

    def __str__(self) -> str:
        """Return the __str__.

        Returns:
            the representation
        """
        return self.__repr__()

    @property
    def filename(self) -> str:
        """Return the filename.

        Returns:
            the filename of the source
        """
        return self.filepath.name

    @abstractmethod
    def to_dict(self) -> Dict[Any, Any]:
        """Convert the source config file to a dict.

        Returns:
            a dict of the config options and values
        """
