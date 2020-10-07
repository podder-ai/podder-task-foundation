import copy
import pickle
from pathlib import Path
from typing import Any


class Object(object):
    supported_extensions = [".pkl"]
    type = "object"

    def __init__(self, data: Any = None):
        self._data = copy.deepcopy(data)

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

    @property
    def data(self):
        return self._data

    @classmethod
    def load(cls, path: Path):
        with path.open(mode='rb') as file:
            data = pickle.load(file)
            return Object(data=data)

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix in cls.supported_extensions:
            return True

        return False
