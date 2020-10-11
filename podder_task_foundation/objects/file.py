from pathlib import Path
from typing import Optional

from .object import Object


class File(Object):
    supported_extensions = []
    type = "file"

    def __init__(self, data: Optional[Path] = None, name: Optional[str] = None):
        super().__init__(data, name)

    def __repr__(self):
        return str(self._data)

    def __str__(self):
        return str(self._data)

    def save(self, path: Path) -> bool:
        pass

    @classmethod
    def load(cls, path: Path, name: Optional[str] = None):
        return cls(data=path, name=cls._get_name(path, name))

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix not in cls.supported_extensions:
            return False

        return True
