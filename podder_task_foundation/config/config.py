import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv

from .config_file import ConfigFile


class Config(object):
    default_path = Path(os.getenv("CONFIG_ROOT_PATH", "./config/"))

    def __getitem__(self, key):
        return self._data[key]

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return str(self._data)

    def __init__(self, mode: str, path: Optional[Path] = None):
        self._data = {}
        self._mode = mode
        self._load_dotenv()
        self._path = path or self.default_path
        self._load_config(self._path)

    @staticmethod
    def _load_dotenv():
        dotenv_path = "./.env"
        load_dotenv(dotenv_path)

    def _load_config(self, path: Path):
        if not path.exists():
            self._data = {}
        else:
            self._data = self._load_config_directory(path)

    def _load_config_directory(self, path: Path) -> Optional[dict]:
        data = {}
        for config in path.iterdir():
            if config.is_dir():
                subdirectory_data = self._load_config_directory(config.resolve())
                if subdirectory_data is not None:
                    data[config.name] = subdirectory_data
            else:
                file = ConfigFile(config.resolve())
                values = file.parse()
                if values is None:
                    continue
                data[config.stem] = values

        return data

    def get(self, key: str, default: Any = None) -> Any:
        paths = key.split('.')
        data = self._data
        for path in paths:
            if path in data:
                data = data[path]
            else:
                return default

        return data

    @staticmethod
    def env(key: str, default: Any = None) -> Optional[str]:
        return os.getenv(key, default)

    @property
    def path(self) -> Path:
        return self._path
