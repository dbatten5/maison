"""Module to define custom errors."""


class NoSchemaError(Exception):
    """Raised when validation is attempted but no schema has been provided."""


class BadTomlError(Exception):
    """Raised when loading from an invalid toml source is attempted."""


class UnsupportedConfigError(Exception):
    """Raised when a config is attempted to be parsed but no parser for it was registered."""
