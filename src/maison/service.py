import pathlib
import typing
from collections.abc import Iterable

from maison import types
from maison import utils


class IsSchema(typing.Protocol):
    """Protocol for config schemas."""

    def model_dump(self) -> types.ConfigValues:
        """Convert the validated config to a dict."""
        ...


class Filesystem(typing.Protocol):
    def get_file_path(
        self, file_name: str, starting_path: typing.Optional[pathlib.Path] = None
    ) -> typing.Optional[pathlib.Path]: ...


class ConfigReader(typing.Protocol):
    def parse_config(self, file_path: pathlib.Path) -> types.ConfigValues: ...


class Validator(typing.Protocol):
    def validate(
        self, values: types.ConfigValues, schema: type[IsSchema]
    ) -> types.ConfigValues: ...


class ConfigService:
    def __init__(
        self,
        filesystem: Filesystem,
        config_reader: ConfigReader,
        validator: Validator,
    ) -> None:
        self.filesystem = filesystem
        self.config_reader = config_reader
        self.validator = validator

    def find_configs(
        self,
        source_files: list[str],
        starting_path: typing.Optional[pathlib.Path] = None,
    ) -> Iterable[pathlib.Path]:
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
        config_values: types.ConfigValues = {}

        for path in config_file_paths:
            parsed_config = self.config_reader.parse_config(path)
            config_values = utils.deep_merge(config_values, parsed_config)

            if not merge_configs:
                break

        return config_values

    def validate_config(
        self, values: types.ConfigValues, schema: type[IsSchema]
    ) -> types.ConfigValues:
        return self.validator.validate(values=values, schema=schema)
