import csv
from pathlib import Path
from typing import Optional

from podder_task_foundation.utilities import DataFileLoader

from .text_serializable import TextSerializable


class Array(TextSerializable):
    type = "array"
    supported_object_type = list

    def save(self,
             path: Path,
             encoding: Optional[str] = 'utf-8',
             indent: Optional[int] = None) -> bool:

        file_type = DataFileLoader().get_file_type(path)
        if file_type is None:
            return False

        if file_type == "csv":
            with path.open("w", encoding=encoding, newline="") as file_handler:
                writer = csv.writer(file_handler)
                for row in self.data:
                    writer.writerow(row)
            return True

        return super().save(path, encoding, indent)

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
