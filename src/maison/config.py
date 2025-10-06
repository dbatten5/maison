"""Module to hold the `UserConfig` class definition."""

import pathlib
import typing

from maison import config_parser
from maison import config_validator as validator
from maison import disk_filesystem
from maison import errors
from maison import parsers
from maison import protocols
from maison import service
from maison import typedefs


def _bootstrap_service(package_name: str) -> service.ConfigService:
    _config_parser = config_parser.ConfigParser()

    pyproject_parser = parsers.PyprojectParser(tool_name=package_name)
    toml_parser = parsers.TomlParser()
    ini_parser = parsers.IniParser()

    _config_parser.register_parser(
        suffix=".toml", parser=pyproject_parser, stem="pyproject"
    )
    _config_parser.register_parser(suffix=".toml", parser=toml_parser)
    _config_parser.register_parser(suffix=".ini", parser=ini_parser)

    return service.ConfigService(
        filesystem=disk_filesystem.DiskFilesystem(),
        config_parser=_config_parser,
        validator=validator.Validator(),
    )


class UserConfig:
    """Model the user configuration."""

    def __init__(
        self,
        package_name: str,
        starting_path: typing.Optional[pathlib.Path] = None,
        source_files: typing.Optional[list[str]] = None,
        schema: typing.Optional[type[protocols.IsSchema]] = None,
        merge_configs: bool = False,
    ) -> None:
        """Initialize the config.

        Args:
            package_name: the name of the package, to be used to find the right section
                in the config file
            starting_path: an optional starting path to start the search for config
                file
            source_files: an optional list of source config filenames or absolute paths
                to search for. If none is provided then `pyproject.toml` will be used.
            schema: an optional `pydantic` model to define the config schema
            merge_configs: an optional boolean to determine whether configs should be
                merged if multiple are found
        """
        self.source_files = source_files or ["pyproject.toml"]
        self.starting_path = starting_path
        self.merge_configs = merge_configs
        self._schema = schema

        self._service = _bootstrap_service(package_name=package_name)

        _sources = self._service.find_configs(
            source_files=self.source_files,
            starting_path=starting_path,
        )

        self._values = self._service.get_config_values(
            config_file_paths=_sources,
            merge_configs=merge_configs,
        )

    def __str__(self) -> str:
        """Return the __str__.

        Returns:
            the string representation
        """
        return f"<class '{self.__class__.__name__}'>"

    @property
    def values(self) -> typedefs.ConfigValues:
        """Return the user's configuration values.

        Returns:
            the user's configuration values
        """
        return self._values

    @values.setter
    def values(self, values: typedefs.ConfigValues) -> None:
        """Set the user's configuration values."""
        self._values = values

    @property
    def discovered_paths(self) -> list[pathlib.Path]:
        """Return a list of the paths to the config sources found on the filesystem.

        Returns:
            a list of the paths to the config sources
        """
        return list(
            self._service.find_configs(
                source_files=self.source_files,
                starting_path=self.starting_path,
            )
        )

    @property
    def path(self) -> typing.Optional[typing.Union[pathlib.Path, list[pathlib.Path]]]:
        """Return the path to the selected config source.

        Returns:
            `None` is no config sources have been found, a list of the found config
            sources if `merge_configs` is `True`, or the path to the active config
            source if `False`
        """
        if len(self.discovered_paths) == 0:
            return None

        if self.merge_configs:
            return self.discovered_paths

        return self.discovered_paths[0]

    @property
    def schema(self) -> typing.Optional[type[protocols.IsSchema]]:
        """Return the schema.

        Returns:
            the schema
        """
        return self._schema

    @schema.setter
    def schema(self, schema: type[protocols.IsSchema]) -> None:
        """Set the schema."""
        self._schema = schema

    def validate(
        self,
        schema: typing.Optional[type[protocols.IsSchema]] = None,
        use_schema_values: bool = True,
    ) -> typedefs.ConfigValues:
        """Validate the configuration.

        Warning:
            Using this method with `use_schema_values` set to `True` will cast values to
            whatever is defined in the schema. For example, for the following schema:

                class Schema(ConfigSchema):
                    foo: str

            Validating a config with:

                {"foo": 1}

            Will result in:

                {"foo": "1"}

        Args:
            schema: an optional class that follows the `IsSchema` protocol that
                defines the schema. This takes precedence over a schema provided at
                object instantiation.
            use_schema_values: an optional boolean to indicate whether the result
                of passing the config through the schema should overwrite the existing
                config values, meaning values are cast to types defined in the schema as
                described above, and default values defined in the schema are used.

        Returns:
            the config values

        Raises:
            NoSchemaError: when validation is attempted but no schema has been provided
        """
        selected_schema: typing.Union[type[protocols.IsSchema], None] = (
            schema or self.schema
        )

        if not selected_schema:
            raise errors.NoSchemaError

        validated_values = self._service.validate_config(
            values=self.values, schema=selected_schema
        )

        if use_schema_values:
            self.values = validated_values

        return self.values
