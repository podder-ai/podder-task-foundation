from typing import Any, Dict, Optional

from .exceptions import ImmutableObjectError


class DataBag(object):
    _IS_IMMUTABLE = False

    def __getitem__(self, key):
        return self._data[key]

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return str(self._data)

    def __init__(self, data: Optional[Dict] = None):
        self._data = data if data is not None else {}

    def get(self, key: Optional[str] = None, default: Any = None) -> Any:
        if key is None:
            return self._data
        paths = key.split('.')
        data = self._data
        for path in paths:
            if path in data:
                data = data[path]
            else:
                return default

        return data

    def set(self, key: str, value: Any):
        if self._IS_IMMUTABLE:
            raise ImmutableObjectError()

        paths = key.split('.')
        data = self._data
        for index, path in enumerate(paths):
            if index == len(paths) - 1:
                data[path] = value
            else:
                if path not in data:
                    data[path] = {}
                data = data[path]

        return data
