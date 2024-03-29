from pathlib import Path
from typing import Any, Optional, Type

from ..plugin import ObjectPluginManager
from .array import Array
from .csv import CSV
from .dictionary import Dictionary
from .directory import Directory
from .file import File
from .object import Object
from .text import Text

_objects = ObjectPluginManager().get_classes()
_objects.extend([Text, Dictionary, Array, CSV, Directory])


def factory(_file: Path) -> Optional[Object]:
    for data_type in _objects:
        if data_type.is_supported_file(_file):
            return data_type.load(_file)

    return File.load(_file)


def factory_from_object(_object: Any, name: Optional[str] = None) -> Optional[Object]:
    for data_type in _objects:
        if data_type.is_supported_object(_object):
            return data_type(data=_object, name=name)

    return None


def get_class_from_type(_type: str) -> Optional[Type[Object]]:
    for data_type in _objects:
        if data_type.type == _type:
            return data_type

    return None
