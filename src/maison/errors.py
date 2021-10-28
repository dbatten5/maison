"""Module to define custom errors."""


class NoSchemaError(Exception):
    """Raised when validation is attempted but no schema has been provided."""
