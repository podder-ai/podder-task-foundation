import json
from pathlib import Path
from typing import Optional

import yaml

from podder_task_foundation.utilities import DataFileLoader

from ..utilities import NumpyJsonEncoder
from .object import Object


class TextSerializable(Object):
    supported_extensions = [".json", ".yaml", ".yml"]
    default_extension = ".json"

    def __repr__(self):
        return self.to_json()

    def __str__(self):
        return self.to_json()

    def __getitem__(self, item):
        return self.data[item]

    def to_yaml(self, indent: Optional[int] = None) -> str:
        return yaml.dump(self.data, indent=indent, allow_unicode=True)

    def to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.data, cls=NumpyJsonEncoder, ensure_ascii=False, indent=indent)

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

    def _lazy_load(self):
        self._data = DataFileLoader().load(self.path)

    @classmethod
    def load(cls, path: Path, name: Optional[str] = None):
        return cls(None, path=path, name=cls._get_name(path, name))
