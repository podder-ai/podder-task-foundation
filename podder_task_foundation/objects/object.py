import copy
import pickle
import shutil
from pathlib import Path
from typing import Any, Optional, Union

from ..utilities import Strings


class Object(object):
    supported_extensions = [".pkl"]
    type = "object"
    default_extension = ".pkl"
    supported_object_type = None

    def __init__(self,
                 data: Any = None,
                 path: Union[None, Path, str] = None,
                 name: Optional[str] = None):

        try:
            self._data = copy.deepcopy(data) if data is not None else None
        except TypeError:
            self._data = copy.copy(data)

        if type(path) == str and path != "":
            self._path = Path(path)
        elif isinstance(path, Path):
            self._path = path
        else:
            self._path = None

        if name is None or name == "":
            if self._path is not None:
                name = self._path.name
            else:
                name = Strings().random_string(16)
        self._name = name

    def __repr__(self):
        return self.to_repr()

    def __str__(self):
        return self.to_str()

    def _lazy_load(self):
        pass

    def to_repr(self) -> str:
        return "<Type: {}>".format(self.type)

    def to_str(self) -> str:
        return "<Type: {}>".format(self.type)

    def to_dict(self) -> dict:
        return {}

    @property
    def data(self) -> Any:
        if self._data is None and self._path is not None:
            self._lazy_load()
        return self._data

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> Optional[Path]:
        return self._path

    @property
    def extension(self) -> str:
        if isinstance(self._path, Path):
            return self._path.suffix
        return ""

    def save(self,
             path: Path,
             encoding: Optional[str] = 'utf-8',
             indent: Optional[int] = None) -> bool:

        if self.path is not None:
            shutil.copy(self.path, path)
            return True

        if self._data is None:
            path.touch()
            return True

        try:
            with path.open(mode='wb') as file:
                pickle.dump(self._data, file)
        except TypeError:
            path.write_text("Can't pickle this object")
        except AttributeError:
            path.write_text("Can't pickle this object")

        return True

    def clear(self):
        self._data = None

    def copy(self, path: Path) -> bool:
        if self.path is None:
            return self.save(path)
        else:
            shutil.copy(self.path, path)

        return True

    def rename(self, name: str):
        self._name = name

    def get_file_name(self, base_path: Optional[Path] = None) -> Path:
        path = Path(self._name)
        if path.suffix == "":
            path = path.parent.joinpath(self.name + self.default_extension)
        if path.suffix not in self.supported_extensions:
            path = path.parent.joinpath(path.name + self.default_extension)
        if base_path is not None:
            path = base_path.joinpath(path.name)

        return path

    @classmethod
    def load(cls, path: Path, name: Optional[str] = None) -> "Object":
        return cls(path=path, name=cls._get_name(path, name))

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix in cls.supported_extensions:
            return True

        return False

    @classmethod
    def is_supported_object(cls, _object: Any) -> bool:
        if cls.supported_object_type is None:
            return False
        if isinstance(_object, cls.supported_object_type):
            return True
        return False

    @classmethod
    def _get_name(cls, path: Path, name: Optional[str] = None) -> str:
        if name is not None:
            return name

        return path.name

    def get(self, data_format: Optional[str] = None) -> Optional[object]:
        return self.data
