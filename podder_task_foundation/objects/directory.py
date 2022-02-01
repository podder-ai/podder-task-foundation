import shutil
import tempfile
from pathlib import Path
from typing import Optional

from ..exceptions import ProcessError
from .object import Object


class Directory(Object):
    type = "directory"

    def __init__(self, data: Optional[Path] = None, name: Optional[str] = None):
        self._temporary_directory_object = None
        if data is None:
            self._temporary_directory_object = tempfile.TemporaryDirectory(prefix=name)
            data = Path(self._temporary_directory_object.name)

        super().__init__(data=data, name=name, path=data)

    def __del__(self):
        if self._temporary_directory_object is not None:
            self._temporary_directory_object.cleanup()

    def __repr__(self):
        return str(self._data)

    def __str__(self):
        return str(self._data)

    def get_file(self, name: str) -> Path:
        return self.path.joinpath(name)

    def add_file(self, _object: Object):
        _object.save(self.path.joinpath(_object.name))

    def save(self,
             path: Path,
             encoding: Optional[str] = 'utf-8',
             indent: Optional[int] = None) -> bool:
        shutil.copytree(self.path, path)

        return True

    def copy(self, path: Path) -> bool:
        if self.path is None:
            return self.save(path)
        else:
            shutil.copytree(self.path, path)

        return True

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
