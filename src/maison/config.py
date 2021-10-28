"""Module to hold the `ProjectConfig` class definition."""
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type

from maison.schema import ConfigSchema
from maison.utils import _find_config


class ProjectConfig:
    """Defines the `ProjectConfig` and provides accessors to get config values."""

    def __init__(
        self,
        project_name: str,
        starting_path: Optional[Path] = None,
        source_files: Optional[List[str]] = None,
        schema: Optional[Type[ConfigSchema]] = None,
    ) -> None:
        """Initialize the config.

        Args:
            project_name: the name of the project, to be used to find the right section
                in the config file
            starting_path: an optional starting path to start the search for config
                file
            source_files: an optional list of source config filenames to search for. If
                none is provided then `pyproject.toml` will be used
            schema: an optional `pydantic` model to define the config schema
        """
        self.source_files = source_files or ["pyproject.toml"]
        config_path, config_dict = _find_config(
            project_name=project_name,
            source_files=self.source_files,
            starting_path=starting_path,
        )
        self._config_dict: Dict[str, Any] = config_dict or {}
        self.config_path: Optional[Path] = config_path
        self.schema = schema

    def __repr__(self) -> str:
        """Return the __repr__.

        Returns:
            the representation
        """
        return f"{self.__class__.__name__} (config_path={self.config_path})"

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

    def validate(
        self,
        schema: Optional[Type[ConfigSchema]] = None,
        use_schema_values: bool = True,
    ) -> None:
        """Validate the configuration.

        Note that this will cast values to whatever is defined in the schema. For
        example, for the following schema:

            class Schema(ConfigSchema):
                foo: str

        Validating a config with:

            {"foo": 1}

        Will result in:

            {"foo": "1"}

        Args:
            schema: an optional `pydantic` base model to define the schema. This takes
                precedence over a schema provided at object instantiation.
            use_schema_values: an optional boolean to indicate whether the result
                of passing the config through the schema should overwrite the existing
                config values, meaning values are cast to types defined in the schema as
                described above, and default values defined in the schema are used.
        """
        validated_schema: Optional[ConfigSchema] = None

        if schema:
            validated_schema = schema(**self._config_dict)
        elif self.schema:
            validated_schema = self.schema(**self._config_dict)

        if validated_schema and use_schema_values:
            self._config_dict = validated_schema.dict()

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
