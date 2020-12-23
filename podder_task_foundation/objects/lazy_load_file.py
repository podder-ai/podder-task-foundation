from pathlib import Path
from typing import Any, Optional

from .object import Object


class LazyLoadFile(Object):
    supported_extensions = []
    type = "lazy_load_file"

    def __init__(self, data: Any = None, path: Optional[Path] = None, name: Optional[str] = None):
        super().__init__(data, name)
        self._path = path

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)

    def _lazy_load(self):
        pass

    def clear(self):
        self._data = ""

    def save(self, path: Path) -> bool:
        pass

    @property
    def data(self):
        if self._data is None:
            self._lazy_load()
        return self._data

    @classmethod
    def load(cls, path: Path, name: Optional[str] = None):
        return cls(path=path, name=cls._get_name(path, name))

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix not in cls.supported_extensions:
            return False

        return True

    def get(self, data_type: Optional[str] = None) -> Optional[object]:
        return self.data
