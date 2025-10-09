"""Holds protocols used throughout the package."""

import pathlib
import typing

from maison import typedefs


class IsSchema(typing.Protocol):
    """Protocol for config schemas."""

    def model_dump(self) -> typedefs.ConfigValues:
        """Convert the validated config to a dict."""
        ...


class Filesystem(typing.Protocol):
    """Defines the interface for a class that interacts with a filesystem."""

    def get_file_path(
        self, file_name: str, starting_path: typing.Optional[pathlib.Path] = None
    ) -> typing.Optional[pathlib.Path]:
        """Search for a file by traversing up a filesystem from a path.

        Args:
            file_name: the name of the file or an absolute path to a config to search for
            starting_path: an optional path from which to start searching

        Returns:
            The `Path` to the file if it exists or `None` if it doesn't
        """
        ...

    def open_file(self, path: pathlib.Path) -> typing.BinaryIO:
        """Open a file.

        Args:
            path: the path to the file

        Returns:
            the opened file as a binary I/O stream
        """
        ...


class ConfigParser(typing.Protocol):
    """Defines the interface for a class that parses a config."""

    def parse_config(
        self,
        file_path: pathlib.Path,
        file: typing.BinaryIO,
    ) -> typedefs.ConfigValues:
        """Parse a config.

        Args:
            file_path: the path to a config file.
            file: the binary I/O stream of the file.

        Returns:
            the parsed config
        """
        ...


class Validator(typing.Protocol):
    """Defines the interface for a class that validates some config values."""

    def validate(
        self, values: typedefs.ConfigValues, schema: type[IsSchema]
    ) -> typedefs.ConfigValues:
        """Validate a config.

        Args:
            values: the config values
            schema: a schema against which to validate the config values

        Returns:
            the validated values
        """
        ...
