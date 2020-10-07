from pathlib import Path
from typing import Optional

from PIL import Image as PILImage
from PIL import ImageOps

from .object import Object


class Image(Object):
    supported_extensions = [
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff"
    ]
    type = "image"

    def __init__(self,
                 data: Optional[object] = None,
                 path: Optional[Path] = None):
        raw_data = None
        if data is not None:
            raw_data = ImageOps.exif_transpose(data)
        elif path is not None:
            raw_data = PILImage.open(str(path))
            raw_data = ImageOps.exif_transpose(raw_data)
        super().__init__(raw_data)

    def __repr__(self):
        return self.to_repr()

    def __str__(self):
        return self.to_str()

    def to_repr(self) -> str:
        return "<Type: {} Format:{} Size:{} Mode:{}>".format(
            self.type, self._data.format, self._data.size, self._data.mode)

    def to_str(self) -> str:
        return "<Type: {} Format:{} Size:{} Mode:{}>".format(
            self.type, self._data.format, self._data.size, self._data.mode)

    def save(self, path: Path):
        if path.suffix == ".jpg" or path.suffix == ".jpeg":
            self._data.save(str(path), quality=90)
        else:
            self._data.save(str(path))

    @classmethod
    def load(cls, path: Path):
        return Image(path=path)
