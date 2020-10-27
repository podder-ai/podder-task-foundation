import shutil
import tempfile
from pathlib import Path
from typing import Optional

from ..config import Config


class TemporaryFile(object):
    def __init__(self, config: Config, base_path=Optional[Path]):
        self._config = config
        self._base_path = base_path or Path(
            self._config.get('file.temporary_directory', default=None))

        self._temporary_directory_object = tempfile.TemporaryDirectory(dir=self._base_path)
        self._temporary_directory = Path(self._temporary_directory_object.name)

    def __del__(self):
        if self._temporary_directory_object is not None:
            self._temporary_directory_object.cleanup()
