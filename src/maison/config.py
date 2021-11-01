"""Module to hold the `ProjectConfig` class definition."""
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type

from maison.errors import NoSchemaError
from maison.schema import ConfigSchema
from maison.utils import _find_config


class ProjectConfig:
    """Defines the `ProjectConfig` and provides accessors to get config values."""

    def __init__(
        self,
        project_name: str,
        starting_path: Optional[Path] = None,
        source_files: Optional[List[str]] = None,
        config_schema: Optional[Type[ConfigSchema]] = None,
    ) -> None:
        """Initialize the config.

        Args:
            project_name: the name of the project, to be used to find the right section
                in the config file
            starting_path: an optional starting path to start the search for config
                file
            source_files: an optional list of source config filenames to search for. If
                none is provided then `pyproject.toml` will be used
            config_schema: an optional `pydantic` model to define the config schema
        """
        self.source_files = source_files or ["pyproject.toml"]
        config_path, config_dict = _find_config(
            project_name=project_name,
            source_files=self.source_files,
            starting_path=starting_path,
        )
        self._config_dict: Dict[str, Any] = config_dict or {}
        self.config_path: Optional[Path] = config_path
        self._config_schema: Optional[Type[ConfigSchema]] = config_schema

    def __repr__(self) -> str:
        """Return the __repr__.

        Returns:
            the representation
        """
        return f"<{self.__class__.__name__} config_path:{self.config_path}>"

    def __str__(self) -> str:
        """Return the __str__.

        Returns:
            the representation
        """
        return self.__repr__()

    def to_dict(self) -> Dict[str, Any]:
        """Return a dict of all the config options.

        Returns:
            a dict of the config options
        """
        return self._config_dict

    @property
    def config_schema(self) -> Optional[Type[ConfigSchema]]:
        """Return the `config_schema`.

        Returns:
            the `config_schema`
        """
        return self._config_schema

    @config_schema.setter
    def config_schema(self, config_schema: Type[ConfigSchema]) -> None:
        """Set the `config_schema`."""
        self._config_schema = config_schema

    def validate(
        self,
        config_schema: Optional[Type[ConfigSchema]] = None,
        use_schema_values: bool = True,
    ) -> Dict[str, Any]:
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
            config_schema: an optional `ConfigSchema` to define the schema. This
                takes precedence over a schema provided at object instantiation.
            use_schema_values: an optional boolean to indicate whether the result
                of passing the config through the schema should overwrite the existing
                config values, meaning values are cast to types defined in the schema as
                described above, and default values defined in the schema are used.

        Returns:
            the config values

        Raises:
            NoSchemaError: when validation is attempted but no schema has been provided
        """
        if not (config_schema or self.config_schema):
            raise NoSchemaError

        schema: Type[ConfigSchema] = config_schema or self.config_schema  # type: ignore

        validated_schema: ConfigSchema = schema(**self._config_dict)

        if use_schema_values:
            self._config_dict = validated_schema.dict()

        return self._config_dict

    def get_option(
        self, option_name: str, default_value: Optional[Any] = None
    ) -> Optional[Any]:
        """Return the value of a config option.

        Args:
            option_name: the config option for which to return the value
            default_value: an option default value if the option isn't set

        Returns:
            The value of the given config option or `None` if it doesn't exist
        """
        return self._config_dict.get(option_name, default_value)
