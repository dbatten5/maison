"""Holds the definition of the main service class."""

import pathlib
import typing
from collections.abc import Iterable

from maison import protocols
from maison import types
from maison import utils


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


class ConfigParser(typing.Protocol):
    """Defines the interface for a class that parses a config."""

    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues:
        """Parse a config.

        Args:
            file_path: the path to a config file.

        Returns:
            the parsed config
        """
        ...


class Validator(typing.Protocol):
    """Defines the interface for a class that validates some config values."""

    def validate(
        self, values: types.ConfigValues, schema: type[protocols.IsSchema]
    ) -> types.ConfigValues:
        """Validate a config.

        Args:
            values: the config values
            schema: a schema against which to validate the config values

        Returns:
            the validated values
        """
        ...


class ConfigService:
    """The main service class."""

    def __init__(
        self,
        filesystem: Filesystem,
        config_parser: ConfigParser,
        validator: Validator,
    ) -> None:
        """Initialize the class.

        Args:
            filesystem: a concretion of the `Filesystem` interface
            config_parser: a concretion of the `ConfigParser` interface
            validator: a concretion of the `Validator` interface
        """
        self.filesystem = filesystem
        self.config_parser = config_parser
        self.validator = validator

    def find_configs(
        self,
        source_files: list[str],
        starting_path: typing.Optional[pathlib.Path] = None,
    ) -> Iterable[pathlib.Path]:
        """Find configs in the filesystem.

        Args:
            source_files: a list of file names or file paths to look for
            starting_path: an optional starting path to start looking

        Yields:
            An iterator of found config files.
        """
        for source in source_files:
            if filepath := self.filesystem.get_file_path(
                file_name=source, starting_path=starting_path
            ):
                yield filepath

    def get_config_values(
        self,
        config_file_paths: Iterable[pathlib.Path],
        merge_configs: bool,
    ) -> types.ConfigValues:
        """Get the values from config files.

        Args:
            config_file_paths: an iterable of file paths for config files
            merge_configs: whether or not to merge config values. If yes, the
                configs are merged from right to left

        Returns:
            The values from the config file(s)
        """
        config_values: types.ConfigValues = {}

        for path in config_file_paths:
            parsed_config = self.config_parser.parse_config(path)
            config_values = utils.deep_merge(config_values, parsed_config)

            if not merge_configs:
                break

        return config_values

    def validate_config(
        self, values: types.ConfigValues, schema: type[protocols.IsSchema]
    ) -> types.ConfigValues:
        """Validate config values against a schema.

        Args:
            values: the values to validate
            schema: the schema against which to validate the values

        Returns:
            the validated values
        """
        return self.validator.validate(values=values, schema=schema)
