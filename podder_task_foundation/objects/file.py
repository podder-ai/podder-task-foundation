from pathlib import Path
from typing import Optional

from .object import Object


class File(Object):
    supported_extensions = []
    type = "file"

    def __init__(self, data: Optional[Path] = None):
        super().__init__(data)

    def __repr__(self):
        return str(self._data)

    def __str__(self):
        return str(self._data)

    def save(self, path: Path) -> bool:
        pass

    @classmethod
    def load(cls, path: Path):
        return cls(path)

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix not in cls.supported_extensions:
            return False

        return True
