import json
from pathlib import Path
from typing import List, Optional

import yaml

from podder_task_foundation.utilities import DataFileLoader

from .object import Object


class Array(Object):
    supported_extensions = [".json", ".yaml", ".csv"]
    type = "array"

    def __init__(self, data: Optional[List] = None):
        super().__init__(data)

    def __repr__(self):
        return self.to_json()

    def __str__(self):
        return self.to_json()

    def __getitem__(self, item):
        return self._data[item]

    def to_json(self) -> str:
        return json.dumps(self._data)

    def save(self, path: Path) -> bool:
        file_type = DataFileLoader().get_file_type(path)
        if file_type is None:
            return False

        if file_type == "yaml":
            path.write_text(yaml.dump(self._data))
            return True

        if file_type == "json":
            path.write_text(json.dumps(self._data))
            return True

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
            if data[0] == "[":
                return True

        if file_type == "yaml":
            data = data.strip()
            if data[0] == "-":
                return True

        return False
