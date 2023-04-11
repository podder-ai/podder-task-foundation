from pathlib import Path
from typing import Optional

from .config import Config
from .config_file import ConfigFile


class SharedConfig(Config):

    def _load_config_directory(self, path: Path) -> Optional[dict]:
        data = {}
        for config in path.iterdir():
            if config.is_dir():
                if str(self._path) != str(path) or (str(self._path) == str(path)
                                                    and not self._check_process_name(config.name)):
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

    @staticmethod
    def _check_process_name(name: str) -> bool:
        path = Path("./processes/").joinpath(name)
        return path.exists()
