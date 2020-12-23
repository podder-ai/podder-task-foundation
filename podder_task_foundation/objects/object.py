import copy
import pickle
from pathlib import Path
from typing import Any, Optional, Union

from ..utilities import Strings


class Object(object):
    supported_extensions = [".pkl"]
    type = "object"
    default_extension = ".pkl"

    def __init__(self,
                 data: Any = None,
                 path: Union[None, Path, str] = None,
                 name: Optional[str] = None):
        self._data = copy.deepcopy(data)

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

    def to_repr(self) -> str:
        return "<Type: {}>".format(self.type)

    def to_str(self) -> str:
        return "<Type: {}>".format(self.type)

    def to_dict(self) -> dict:
        return {}

    @property
    def data(self) -> Any:
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

    def save(self, path: Path) -> bool:
        with path.open(mode='wb') as file:
            pickle.dump(self._data, file)

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
    def load(cls, path: Path, name: Optional[str] = None):
        with path.open(mode='rb') as file:
            data = pickle.load(file)
            return Object(data=data, name=cls._get_name(path, name))

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix in cls.supported_extensions:
            return True

        return False

    @classmethod
    def _get_name(cls, path: Path, name: Optional[str] = None) -> str:
        if name is not None:
            return name

        return path.name

    def get(self, data_type: Optional[str] = None) -> Optional[object]:
        return self._data
