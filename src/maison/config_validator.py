"""Holds the tools for validating a user's config."""

from maison import protocols
from maison import typedefs


class Validator:
    """A utility class for validating a user's config.

    Implements the `Validator` protocol.
    """

    def validate(
        self, values: typedefs.ConfigValues, schema: type[protocols.IsSchema]
    ) -> typedefs.ConfigValues:
        """See `Validator.validate`."""
        validated_schema = schema(**values)
        return validated_schema.model_dump()
