import json
from collections import OrderedDict
from pathlib import Path
from typing import Optional

import yaml

from podder_task_foundation.utilities import DataFileLoader

from ..utilities import NumpyJsonEncoder
from .object import Object


class Dictionary(Object):
    _properties = OrderedDict({})
    supported_extensions = [".json", ".yaml", ".yml"]
    type = "dictionary"
    default_extension = ".json"

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

    def to_yaml(self, indent: Optional[int] = None) -> str:
        return yaml.dump(self._data, indent=indent, allow_unicode=True)

    def to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self._data, cls=NumpyJsonEncoder, ensure_ascii=False, indent=indent)

    def save(self,
             path: Path,
             encoding: Optional[str] = 'utf-8',
             indent: Optional[int] = None) -> bool:

        file_type = DataFileLoader().get_file_type(path)
        if file_type is None:
            return False

        if file_type == "yaml":
            path.write_text(self.to_yaml(indent=indent), encoding=encoding)
            return True

        if file_type == "json":
            path.write_text(self.to_json(indent=indent), encoding=encoding)
            return True

        return False

    @classmethod
    def load(cls, path: Path, name: Optional[str] = None):
        data = DataFileLoader().load(path)
        return cls(data, path=path, name=cls._get_name(path, name))

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
