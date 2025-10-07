"""Holds the definition of the main service class."""

import pathlib
import typing
from collections.abc import Iterable

from maison import protocols
from maison import typedefs
from maison import utils


class ConfigService:
    """The main service class."""

    def __init__(
        self,
        filesystem: protocols.Filesystem,
        config_parser: protocols.ConfigParser,
        validator: protocols.Validator,
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
    ) -> typedefs.ConfigValues:
        """Get the values from config files.

        Args:
            config_file_paths: an iterable of file paths for config files
            merge_configs: whether or not to merge config values. If yes, the
                configs are merged from right to left

        Returns:
            The values from the config file(s)
        """
        config_values: typedefs.ConfigValues = {}

        for path in config_file_paths:
            file = self.filesystem.open_file(path=path)
            parsed_config = self.config_parser.parse_config(file_path=path, file=file)
            config_values = utils.deep_merge(config_values, parsed_config)

            if not merge_configs:
                break

        return config_values

    def validate_config(
        self, values: typedefs.ConfigValues, schema: type[protocols.IsSchema]
    ) -> typedefs.ConfigValues:
        """Validate config values against a schema.

        Args:
            values: the values to validate
            schema: the schema against which to validate the values

        Returns:
            the validated values
        """
        return self.validator.validate(values=values, schema=schema)
