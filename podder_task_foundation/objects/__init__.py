from pathlib import Path
from typing import Optional

from .array import Array
from .csv import CSV
from .dictionary import Dictionary
from .file import File
from .image import Image
from .object import Object
from .pdf import PDF


def factory(_file: Path) -> Optional[Object]:
    if _file.is_dir():
        return None

    for data_type in [PDF, Image, CSV, Dictionary, Array]:
        if data_type.is_supported_file(_file):
            return data_type.load(_file)

    return File.load(_file)


__all__ = ["Object", "Dictionary", "Array", "Image", "PDF", "CSV", "factory"]
