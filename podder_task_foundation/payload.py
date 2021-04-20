import copy
import fnmatch
from pathlib import Path
from typing import Dict, Generator, List, Optional, Union

from .exceptions import WrongDataFormatError
from .objects import CSV, PDF, Array, Dictionary, Image, Object, factory


class Payload(object):
    def __init__(self):
        self._data = []

    def __getitem__(self, name):
        return self.get(name=name)

    @staticmethod
    def _should_be_target(target_object: [Object],
                          name: Optional[str] = None,
                          object_types: Optional[List[str]] = None,
                          extensions: Optional[List[str]] = None) -> True:
        if name is not None and not fnmatch.fnmatch(target_object.name, name):
            return False
        if object_types is not None and target_object.type not in object_types:
            return False
        if extensions is not None and target_object.path is not None and target_object.path.suffix not in extensions:
            return False

        return True

    def _filter(self,
                name: Optional[str] = None,
                object_types: Optional[List[str]] = None,
                extensions: Optional[List[str]] = None) -> [Object]:
        result = []
        for _object in self._data:
            if self._should_be_target(_object, name, object_types, extensions):
                result.append(_object)

        return result

    def _first(self,
               name: Optional[str] = None,
               object_types: Optional[List[str]] = None,
               extensions: Optional[List[str]] = None) -> Optional[Object]:
        for _object in self._data:
            if self._should_be_target(_object, name, object_types, extensions):
                return _object

        return None

    def add_directory(self, directory: Path) -> bool:
        if not directory.is_dir():
            return False
        files = sorted(list(directory.glob("*")), key=lambda x: x.name)

        for file in files:
            if file.is_dir() or file.name[0] == ".":
                continue
            self.add_file(file, name=file.name)

        return True

    def add_file(self, file: Path, name: Optional[str] = None) -> bool:
        if file.is_dir():
            return False
        _object = factory(file)
        if _object is None:
            return False
        self.add(_object, name)

        return True

    def add(self, _object: Object, name: Optional[str] = None):
        if name is not None:
            _object.rename(name)

        self._data.append(_object)

    def add_dictionary(self, dictionary: dict, name: Optional[str] = None):
        if not isinstance(dictionary, dict):
            raise WrongDataFormatError(
                detail="Format is not dict for name {}. Got {}".format(
                    name or "Noname", type(dictionary)),
                how_to_solve="Change format to dict or use appropriate method to add data")
        data = Dictionary(data=dictionary, name=name)
        self.add(data)

    def add_array(self, array: Union[list, Object], name: Optional[str] = None):
        if isinstance(array, CSV):
            self.add(array, name=name)
            return
        if not isinstance(array, list):
            raise WrongDataFormatError(
                detail="Format is not list for name {}. Got {}".format(
                    name or "Noname", type(array)),
                how_to_solve="Change format to dict or use appropriate method to add data")
        data = Array(data=array, name=name)
        self.add(data)

    def add_image(self, image: object, name: Optional[str] = None):
        data = Image(data=image, name=name)
        self.add(data)

    def add_pdf(self, pdf: Path, name: Optional[str] = None):
        data = PDF(data=pdf, name=name)
        self.add(data)

    def all(self,
            name: Optional[str] = None,
            object_type: Union[None, str, List[str]] = None,
            extension: Union[None, str, List[str]] = None) -> [Object]:
        if name is None and object_type is None:
            return self._data
        if object_type is not None and isinstance(object_type, str):
            object_type = [object_type]
        if isinstance(extension, str):
            extension = [extension]
        return self._filter(name=name, object_types=object_type, extensions=extension)

    def get(self,
            name: Optional[str] = None,
            object_type: Union[None, str, List[str]] = None,
            extension: Union[None, str, List[str]] = None) -> Optional[Object]:
        if isinstance(object_type, str):
            object_type = [object_type]
        if isinstance(extension, str):
            extension = [extension]
        return self._first(name=name, object_types=object_type, extensions=extension)

    def get_image(self, name: Optional[str] = None) -> Optional[object]:
        image = self.get(name=name, object_type="image")
        if image is not None:
            return image.data

        return None

    def get_data(self, name: Optional[str] = None) -> Optional[Union[Dict, List]]:
        data = self.get(name, ["dictionary", "array", "csv"])
        if data is not None:
            return data.data

        return None

    def all_images(self, name: Optional[str] = None) -> Generator[object, None, None]:
        images = self.all(name, object_type="image")
        for image in images:
            yield image.data

    def copy(self) -> object:
        return copy.deepcopy(self)

    def merge(self, target):
        for _object in target.all():
            self.add(_object)

        return
4