import urllib
from functools import reduce


def flatten(d):
    """Return a dict as a list of lists.

    >>> flatten({"a": "b"})
    [['a', 'b']]
    >>> flatten({"a": {"b": "c"}})
    [['a', 'b', 'c']]
    >>> flatten({"a": {"b": {"c": "e"}}})
    [['a', 'b', 'c', 'e']]
    >>> flatten({"a": {"b": "c", "d": "e"}})
    [['a', 'b', 'c'], ['a', 'd', 'e']]

    """

    if not isinstance(d, dict):
        return d

    returned = []
    for key, value in d.items():
        # Each key, value is treated as a row.
        current_row = [key]
        current_row.extend(flatten(value))
        returned.append(current_row)

    return returned


def parametrize(params):
    """Return list of params as params.

    >>> parametrize(['a'])
    'a'
    >>> parametrize(['a', 'b'])
    'a[b]'
    >>> parametrize(['a', 'b', 'c'])
    'a[b][c]'

    """
    returned = params[0]
    returned += "".join("[" + p + "]" for p in params[1:])
    return returned


def urlencode(params):
    """Urlencode a multidimensional dict."""

    # Not doing duck typing here. Will make debugging easier.
    if not isinstance(params, dict):
        raise TypeError("Only dict are supported for now.")

    params = flatten(params)

    url_params = {}
    for param in params:
        value = params.pop()
        url_params[parametrize(params)] = value

    return urllib.urlencode(url_params)
