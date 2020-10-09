from pathlib import Path
from typing import Optional

from .array import Array
from .dictionary import Dictionary
from .image import Image
from .object import Object
from .pdf import PDF


def factory(file: Path) -> Optional[Object]:
    if file.is_dir():
        return None

    for data_type in [PDF, Image, Dictionary, Array]:
        if data_type.is_supported_file(file):
            return data_type.load(file)

    return None


__all__ = ["Object", "Dictionary", "Array", "Image", "PDF", "factory"]
