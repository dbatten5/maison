"""Holds type definitions that are used across the package."""

import typing


ConfigValues = dict[str, typing.Union[str, int, float, bool, None, "ConfigValues"]]
