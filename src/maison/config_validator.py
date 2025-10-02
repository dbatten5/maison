"""Holds the tools for validating a user's config."""

from maison import protocols
from maison import types


class Validator:
    """A utility class for validating a user's config.

    Implements the `Validator` protocol.
    """

    def validate(
        self, values: types.ConfigValues, schema: type[protocols.IsSchema]
    ) -> types.ConfigValues:
        """See `Validator.validate`."""
        validated_schema = schema(**values)
        return validated_schema.model_dump()
