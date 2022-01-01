import csv
import json
from pathlib import Path
from typing import Optional

import yaml

from podder_task_foundation.utilities import DataFileLoader

from ..utilities import NumpyJsonEncoder
from .object import Object


class Array(Object):
    supported_extensions = [".json", ".yaml"]
    type = "array"
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

        if file_type == "csv":
            with path.open("w", encoding=encoding, newline="") as file_handler:
                writer = csv.writer(file_handler)
                for row in self._data:
                    writer.writerow(row)
            return True

        return False

    @classmethod
    def load(cls, path: Path, name: Optional[str] = None) -> Object:
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
            if data[0] == "[":
                return True

        if file_type == "yaml":
            data = data.strip()
            if data[0] == "-":
                return True

        return False
