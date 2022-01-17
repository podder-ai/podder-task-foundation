import shutil
import tempfile
from pathlib import Path
from typing import Optional

from .object import Object


class File(Object):
    supported_extensions = []
    type = "file"

    def __init__(self, data: Optional[Path] = None, name: Optional[str] = None):
        self._temporary_directory_object = tempfile.TemporaryDirectory(prefix=name)
        copied_file_path = Path(self._temporary_directory_object.name).joinpath(data.name)
        shutil.copy(data, copied_file_path)
        super().__init__(data=copied_file_path, name=name, path=copied_file_path)

    def __del__(self):
        if self._temporary_directory_object is not None:
            self._temporary_directory_object.cleanup()

    def __repr__(self):
        return str(self._data)

    def __str__(self):
        return str(self._data)

    def save(self,
             path: Path,
             encoding: Optional[str] = 'utf-8',
             indent: Optional[int] = None) -> bool:
        shutil.copy(self._data, path)

        return True

    def get_file_name(self, base_path: Optional[Path] = None) -> Path:
        return self._path

    @classmethod
    def load(cls, path: Path, name: Optional[str] = None) -> Object:
        return cls(data=path, name=cls._get_name(path, name))

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix not in cls.supported_extensions:
            return False

        return True
