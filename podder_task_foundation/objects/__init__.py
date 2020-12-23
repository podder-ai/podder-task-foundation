from pathlib import Path
from typing import Optional

from .array import Array
from .dictionary import Dictionary
from .file import File
from .object import Object
from .pdf import PDF
from .lazy_load_file import LazyLoadFile
from ..plugin import PluginManager


_filetypes = PluginManager().get_filetype_classes()
_filetypes.extend([PDF, Dictionary, Array])


def factory(_file: Path) -> Optional[Object]:
    if _file.is_dir():
        return None

    for data_type in _filetypes:
        if data_type.is_supported_file(_file):
            return data_type.load(_file)

    return File.load(_file)


__all__ = ["Object", "Dictionary", "Array", "PDF", "LazyLoadFile", "factory"]
