from pathlib import Path
from typing import Optional

from PIL import Image as PILImage, ImageOps

from .lazy_load_file import LazyLoadFile
from .object import Object


class Image(LazyLoadFile):
    supported_extensions = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff"]
    type = "image"
    default_extension = ".png"

    def __init__(self,
                 data: Optional[object] = None,
                 path: Optional[Path] = None,
                 name: Optional[str] = None):
        raw_data = None
        if data is not None:
            raw_data = ImageOps.exif_transpose(data)
        super().__init__(raw_data, path, name)

    def __repr__(self):
        return self.to_repr()

    def __str__(self):
        return self.to_str()

    def to_repr(self) -> str:
        return "<Type: {} Format:{} Size:{} Mode:{}>".format(self.type, self.data.format,
                                                             self.data.size, self.data.mode)

    def to_str(self) -> str:
        return "<Type: {} Format:{} Size:{} Mode:{}>".format(self.type, self.data.format,
                                                             self.data.size, self.data.mode)

    def _lazy_load(self):
        raw_data = PILImage.open(str(self._path))
        self._data = ImageOps.exif_transpose(raw_data)

    def save(self, path: Path):
        if path.suffix == ".jpg" or path.suffix == ".jpeg":
            self.data.save(str(path), quality=90)
        else:
            self.data.save(str(path))
