import csv
import json
from pathlib import Path
from typing import Optional

import yaml

from podder_task_foundation.utilities import DataFileLoader

from ..utilities import NumpyJsonEncoder
from .object import Object


class Text(Object):
    supported_extensions = [".text", ".txt"]
    type = "text"
    default_extension = ".txt"

    def save(self,
             path: Path,
             encoding: Optional[str] = 'utf-8',
             indent: Optional[int] = None) -> bool:

        file_type = DataFileLoader().get_file_type(path)
        if file_type is None:
            return False

        if file_type == "text":
            path.write_text(self.data, encoding=encoding)

        if file_type == "yaml":
            path.write_text(self.to_yaml(indent=indent), encoding=encoding)
            return True

        if file_type == "json":
            path.write_text(self.to_json(indent=indent), encoding=encoding)
            return True

        return False

    def to_text(self) -> str:
        return self.data.join("\n") if isinstance(self.data, list) else self.data

    def to_yaml(self, indent: Optional[int] = None) -> str:
        return yaml.dump(self.data, indent=indent, allow_unicode=True)

    def to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.data, cls=NumpyJsonEncoder, ensure_ascii=False, indent=indent)

    def to_array(self) -> [str]:
        return self.data.strip().split("\n")

    def _lazy_load(self):
        if self._data is None:
            if self.path is not None:
                self._data = self.path.read_text()
            else:
                self._data = ""
