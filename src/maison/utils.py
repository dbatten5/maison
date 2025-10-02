"""Module to hold various utils."""

from maison import typedefs


def deep_merge(
    destination: typedefs.ConfigValues, source: typedefs.ConfigValues
) -> typedefs.ConfigValues:
    """Recursively updates the destination dictionary.

    Usage example:
    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> deep_merge(a, b) == {
    ...     "first": {"all_rows": {"pass": "dog", "fail": "cat", "number": "5"}}
    ... }

    Note that the arguments may be modified!

    Based on https://stackoverflow.com/a/20666342

    Args:
        destination: A dictionary to be merged into. This will be updated in place.
        source: The dictionary supplying data

    Returns:
        The updated destination dictionary.

    Raises:
        RuntimeError: A dict cannot be merged on top of a non-dict.
            For example, the following would fail:
            `deep_merge({"foo": "bar"}, {"foo": {"baz": "qux"}})`
    """
    for key, src_value in source.items():
        if isinstance(src_value, dict):
            # get node or create one
            dest_node = destination.setdefault(key, {})
            if not isinstance(dest_node, dict):
                raise RuntimeError(
                    f"Cannot merge dict '{src_value}' into type '{type(dest_node)}'"
                )
            _ = deep_merge(dest_node, src_value)
        else:
            destination[key] = src_value

    return destination
