import copy
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Optional

from podder_task_foundation.utilities import DataFileLoader

from ..utilities import NumpyJsonEncoder
from .object import Object


class Dictionary(Object):
    _properties = OrderedDict({})
    supported_extensions = [".json", ".yaml", ".yml"]
    type = "dictionary"

    def __init__(self, data: Optional[Dict] = None):
        super().__init__(data)

    def __repr__(self):
        return self.to_json()

    def __str__(self):
        return self.to_json()

    def __getitem__(self, item):
        return self._data[item]

    def __getattr__(self, item):
        if item not in self._data.keys():
            raise AttributeError("'{}' object has no attribute '{}'".format(
                type(self).__name__, item))
        return self._data[item]

    def __contains__(self, item):
        return item in self._data.keys()

    def to_json(self) -> str:
        return json.dumps(self._data, cls=NumpyJsonEncoder, ensure_ascii=False)

    def save(self, path: Path):
        path.write_text(self.to_json())

    @classmethod
    def load(cls, path: Path):
        data = DataFileLoader().load(path)
        return cls(data)

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix not in cls.supported_extensions:
            return False

        with path.open() as file:
            data = file.read(64)
        data = data.strip()

        file_type = DataFileLoader().get_file_type(path)
        if file_type is None:
            return False

        if file_type == "json":
            if data[0] == "{":
                return True

        if file_type == "yaml":
            data = data.strip()
            if data[0] != "-":
                return True

        return False
