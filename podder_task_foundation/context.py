from pathlib import Path
from typing import Optional

from .config import Config
from .file import File
from .logging.loggers import BaseLogger, ProcessLogger


class Context(object):
    @property
    def config(self) -> Config:
        return self._config

    @property
    def file(self) -> File:
        return self._file

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def logger(self) -> BaseLogger:
        return self._logger

    def __init__(self,
                 mode: str,
                 process_name: Optional[str] = None,
                 config_path: Optional[Path] = None) -> None:
        self._mode = mode
        self._process_name = process_name
        self._config = Config(self._mode, config_path)
        self._file = File(process_name, self._config)
        self._logger = self._get_logger()

    def _get_logger(self) -> BaseLogger:
        return ProcessLogger(self.mode, self._config, self._process_name)
