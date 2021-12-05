import csv
from pathlib import Path
from typing import Any, List, Optional

from .lazy_load_file import LazyLoadFile


class CSV(LazyLoadFile):
    supported_extensions = [".csv"]
    type = "array"
    default_extension = ".csv"

    def __init__(self,
                 data: Optional[object] = None,
                 path: Optional[Path] = None,
                 name: Optional[str] = None):
        super().__init__(data, path, name)
        self._row_type = "array"

    def get(self, data_format: str = "array") -> Any:
        return self._get(row_type=data_format)

    @property
    def data(self) -> Any:
        return self.get(data_format="array")

    def _get(self, row_type: str = "array"):
        if row_type != "array" and row_type != "dict":
            row_type = "array"
        if self._data is None:
            self._row_type = row_type
            self._lazy_load()
        else:
            if self._row_type != row_type:
                self._row_type = row_type
                self._lazy_load()

        return self._data

    def _lazy_load(self):
        if self._row_type == "dict":
            self._data = self._load_as_dict()
        else:
            self._data = self._load_as_array()

    def _load_as_array(self, encoding: Optional[str] = 'utf-8') -> List:
        data = []
        with self._path.open(encoding=encoding) as file_handler:
            reader = csv.reader(file_handler)
            for row in reader:
                data.append(row)

        return data

    def _load_as_dict(self, encoding: Optional[str] = 'utf-8') -> List:
        data = []
        with self._path.open(encoding=encoding) as file_handler:
            reader = csv.DictReader(file_handler)
            for row in reader:
                data.append(row)

        return data

    def save(self,
             path: Path,
             encoding: Optional[str] = 'utf-8',
             indent: Optional[int] = None) -> bool:
        if self._row_type == "dict":
            return self._save_dict(path, encoding)
        else:
            return self._save_array(path, encoding)

    def _save_dict(self, path: Path, encoding: Optional[str] = 'utf-8') -> bool:
        if self.data is None or not isinstance(self.data, list):
            return False
        if len(self.data) == 0:
            path.touch()
            return True

        header = self.data[0].keys()
        with path.open(mode="w", encoding=encoding, newline="") as file_handler:
            writer = csv.DictWriter(file_handler, fieldnames=header)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

        return True

    def _save_array(self, path: Path, encoding: Optional[str] = 'utf-8') -> bool:
        with path.open(mode="w", encoding=encoding, newline="") as file_handler:
            writer = csv.writer(file_handler)
            for row in self.data:
                writer.writerow(row)

        return True
