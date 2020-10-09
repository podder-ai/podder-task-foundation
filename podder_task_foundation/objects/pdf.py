import json
from pathlib import Path
from typing import List, Optional

import yaml

from podder_task_foundation.utilities import DataFileLoader

from .object import Object


class PDF(Object):
    supported_extensions = [".pdf"]
    type = "pdf"

    def __init__(self, data: Optional[Path] = None):
        super().__init__(data)

    def __repr__(self):
        return str(self._data)

    def __str__(self):
        return str(self._data)

    def save(self, path: Path) -> bool:
        pass

    @classmethod
    def load(cls, path: Path):
        return cls(path)

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix not in cls.supported_extensions:
            return False

        return True
