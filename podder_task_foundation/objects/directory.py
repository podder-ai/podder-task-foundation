import shutil
from pathlib import Path
from typing import Optional

from ..exceptions import ProcessError
from .object import Object


class Directory(Object):
    type = "directory"

    def __init__(self, data: Optional[Path] = None, name: Optional[str] = None):
        super().__init__(data=data, name=name, path=data)

    def __repr__(self):
        return str(self._data)

    def __str__(self):
        return str(self._data)

    def get_file(self, name: str) -> Path:
        return self.path.joinpath(name)

    def add_file(self, _object: Object):
        _object.save(self.path.joinpath(_object.name))

    @classmethod
    def load(cls, path: Path, name: Optional[str] = None) -> "Directory":
        if not path.is_dir():
            raise ProcessError("{} is not a directory")

        return cls(data=path, name=cls._get_name(path, name))

    @classmethod
    def create(cls, path: Path, name: Optional[str] = None) -> "Directory":
        if not path.exists():
            path.mkdir()
        return cls.load(path=path, name=cls._get_name(path, name))

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        return path.is_dir()
