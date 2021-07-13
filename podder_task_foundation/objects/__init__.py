from pathlib import Path
from typing import Optional, Type

from ..plugin import ObjectPluginManager
from .array import Array
from .csv import CSV
from .dictionary import Dictionary
from .file import File
from .lazy_load_file import LazyLoadFile
from .object import Object
from .pdf import PDF

_objects = ObjectPluginManager().get_classes()
_objects.extend([PDF, Dictionary, Array, CSV])


def factory(_file: Path) -> Optional[Object]:
    if _file.is_dir():
        return None

    for data_type in _objects:
        if data_type.is_supported_file(_file):
            return data_type.load(_file)

    return File.load(_file)


def get_class_from_type(_type: str) -> Optional[Type[Object]]:
    for data_type in _objects:
        if data_type.type == _type:
            return data_type

    return None


__all__ = [
    "Object", "Dictionary", "Array", "PDF", "LazyLoadFile", "CSV", "factory", "get_class_from_type"
]
