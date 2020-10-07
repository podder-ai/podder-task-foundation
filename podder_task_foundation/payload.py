from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Union

from .objects import Array, Dictionary, Object, factory


class Payload(object):
    def __init__(self):
        self._data = OrderedDict()

    def __getitem__(self, name):
        return self._data[name]

    def add_file(self, file: Path, name: Optional[str] = None) -> bool:
        if file.is_dir():
            return False
        _object = factory(file)
        if _object is None:
            return False

        self.add_object(_object)
        return True

    def add_object(self, _object: Object, name: Optional[str] = None):
        self._data[name] = _object

    def add_dictionary(self, dictionary: dict, name: Optional[str] = None):
        data = Dictionary(data=dictionary)
        self.add_object(data, name=name)

    def add_array(self, array: list, name: Optional[str] = None):
        data = Array(data=array)
        self.add_object(data, name=name)

    def get_all_data(self) -> [Object]:
        return list(self._data.values())

    def get(self, name: str) -> Object:
        return self._data[name]

    def get_image(self, name: Optional[str] = None) -> Optional[object]:
        image = None
        if name is not None:
            if self._data[name].type == "image":
                image = self._data[name]
        else:
            for key in self._data.keys():
                if self._data[key].type == "image":
                    image = self._data[key]

        if image is not None:
            return image.data

        return None

    def get_data(self,
                 name: Optional[str] = None) -> Optional[Union[Dict, List]]:
        data = None
        if name is not None:
            if self._data[name].type == "dictionary" or self._data[
                    name].type == "array":
                data = self._data[name]
        else:
            for key in self._data.values():
                if self._data[name].type == "dictionary" or self._data[
                        name].type == "array":
                    data = self._data[key]

        if data is not None:
            return data.data

        return None
