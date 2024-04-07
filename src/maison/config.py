"""Module to hold the `UserConfig` class definition."""
from collections import UserDict
from functools import reduce
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Protocol
from typing import Type
from typing import Union

from maison.errors import NoSchemaError
from maison.utils import _collect_configs
from maison.utils import deep_merge


class IsSchema(Protocol):
    """Protocol for config schemas."""

    def dict(self) -> Dict[Any, Any]:
        """Convert the validated config to a dict."""
        ...


class UserConfig(UserDict[str, Any]):
    """Model the user configuration."""

    def __init__(
        self,
        project_name: str,
        starting_path: Optional[Path] = None,
        source_files: Optional[List[str]] = None,
        schema: Optional[Type[IsSchema]] = None,
        merge_configs: bool = False,
    ) -> None:
        """Initialize the config.

        Args:
            project_name: the name of the project, to be used to find the right section
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
        self.merge_configs = merge_configs
        self._sources = _collect_configs(
            project_name=project_name,
            source_files=self.source_files,
            starting_path=starting_path,
        )
        self._schema = schema
        super().__init__(**self._generate_config_dict())

    def __str__(self) -> str:
        """Return the __str__.

        Returns:
            the string representation
        """
        return f"<class '{self.__class__.__name__}'>"

    @property
    def discovered_config_paths(self) -> List[Path]:
        """Return a list of the paths to the config sources found on the filesystem.

        Returns:
            a list of the paths to the config sources
        """
        return [source.filepath for source in self._sources]

    @property
    def config_path(self) -> Optional[Union[Path, List[Path]]]:
        """Return a list of the path(s) to the config source(s).

        Returns:
            `None` is no config sources have been found, a list of the found config
            sources if `merge_configs` is `True`, or the path to the active config
            source if `False`
        """
        if len(self._sources) == 0:
            return None

        if self.merge_configs:
            return self.discovered_config_paths

        return self.discovered_config_paths[0]

    @property
    def schema(self) -> Optional[Type[IsSchema]]:
        """Return the schema.

        Returns:
            the schema
        """
        return self._schema

    @schema.setter
    def schema(self, schema: Type[IsSchema]) -> None:
        """Set the schema."""
        self._schema = schema

    def validate(
        self,
        schema: Optional[Type[IsSchema]] = None,
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
        if not (schema or self.schema):
            raise NoSchemaError

        selected_schema: Type[IsSchema] = schema or self.schema  # type: ignore

        validated_schema = selected_schema(**self.data)

        if use_schema_values:
            self.update(validated_schema.dict())

        return self.data

    def _generate_config_dict(self) -> Dict[str, Any]:
        """Generate the project config dict.

        If `merge_configs` is set to `False` then we use the first config. If `True`
        then the dicts of the sources are merged from right to left.

        Returns:
            the project config dict
        """
        if len(self._sources) == 0:
            return {}

        if not self.merge_configs:
            return self._sources[0].to_dict()

        source_dicts = (source.to_dict() for source in self._sources)
        return reduce(lambda a, b: deep_merge(a, b), source_dicts)
