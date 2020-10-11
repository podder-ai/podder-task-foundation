from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Union

from .objects import Array, Dictionary, Image, Object, factory


class Payload(object):
    def __init__(self):
        self._data = OrderedDict()

    def __getitem__(self, name):
        return self._data[name]

    def _filter(self,
                name: Optional[str] = None,
                object_types: Optional[List[str]] = None) -> [Object]:
        result = []
        for key, _object in self._data.items():
            if name is not None and key != name:
                continue
            if object_types is not None and _object.type not in object_types:
                continue
            result.append(_object)

        return result

    def _first(self,
               name: Optional[str] = None,
               object_types: Optional[List[str]] = None) -> Optional[Object]:
        for key, _object in self._data.items():
            if name is not None and key != name:
                continue
            if object_types is not None and _object.type not in object_types:
                continue
            return _object

        return None

    def add_file(self, file: Path, name: Optional[str] = None) -> bool:
        if file.is_dir():
            return False
        _object = factory(file)
        if _object is None:
            return False

        self.add(_object, name)
        return True

    def add(self, _object: Object, name: Optional[str] = None):
        self._data[name] = _object

    def add_dictionary(self, dictionary: dict, name: Optional[str] = None):
        data = Dictionary(data=dictionary)
        self.add(data, name=name)

    def add_array(self, array: list, name: Optional[str] = None):
        data = Array(data=array)
        self.add(data, name=name)

    def add_image(self, image: object, name: Optional[str] = None):
        data = Image(data=image)
        self.add(data, name=name)

    def get_all(self,
                name: Optional[str] = None,
                object_type: Union[None, str, List[str]] = None) -> [Object]:
        if name is None and object_type is None:
            return list(self._data.values())
        if isinstance(object_type, str):
            object_type = [object_type]
        return self._filter(name=name, object_types=object_type)

    def get(self,
            name: Optional[str] = None,
            object_type: Union[None, str, List[str]] = None) -> Object:
        if isinstance(object_type, str):
            object_type = [object_type]
        return self._first(name=name, object_types=object_type)

    def get_image(self, name: Optional[str] = None) -> Optional[object]:
        image = self.get(name=name, object_type="image")
        if image is not None:
            return image.data

        return None

    def get_data(self, name: Optional[str] = None) -> Optional[Union[Dict, List]]:
        data = self.get(name, ["dictionary", "array"])
        if data is not None:
            return data.data

        return None
