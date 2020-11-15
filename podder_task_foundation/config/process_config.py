from pathlib import Path
from typing import Optional

from .config import Config


class ProcessConfig(Config):
    def __init__(self, mode: str, process_name: str, path: Optional[Path] = None):
        path = path or self.default_path
        super().__init__(mode, path.joinpath(process_name))
