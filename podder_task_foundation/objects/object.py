import copy
import pickle
from pathlib import Path
from typing import Any, Optional


class Object(object):
    supported_extensions = [".pkl"]
    type = "object"

    def __init__(self, data: Any = None, name: Optional[str] = None):
        self._data = copy.deepcopy(data)
        self._name = name

    def __repr__(self):
        return self.to_repr()

    def __str__(self):
        return self.to_str()

    def to_repr(self) -> str:
        return "<Type: {}>".format(self.type)

    def to_str(self) -> str:
        return "<Type: {}>".format(self.type)

    def save(self, path: Path):
        with path.open(mode='wb') as file:
            pickle.dump(self._data, file)

    @classmethod
    def _get_name(cls, path: Path, name: Optional[str] = None) -> str:
        if name is not None:
            return name
        name_elements = path.name.split("_")
        return name_elements[0]

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    def rename(self, name: str):
        self._name = name

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
