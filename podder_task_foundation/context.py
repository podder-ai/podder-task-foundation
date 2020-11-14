from pathlib import Path
from typing import Optional

from .config import Config
from .file import File
from .logging.loggers import BaseLogger, ProcessLogger
from .utilities import UID


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
    def job_id(self) -> Optional[str]:
        return self._job_id

    @property
    def process_id(self) -> Optional[str]:
        return self._process_id

    @property
    def process_name(self) -> Optional[str]:
        return self._process_name

    @property
    def logger(self) -> BaseLogger:
        return self._logger

    @property
    def is_process_context(self) -> bool:
        return self._process_name is not None

    def __init__(self,
                 mode: str,
                 process_name: Optional[str] = None,
                 config_path: Optional[Path] = None,
                 logger: Optional[BaseLogger] = None,
                 job_id: Optional[str] = None,
                 process_id: Optional[str] = None) -> None:
        self._mode = mode
        self._job_id = job_id or UID.generate()
        self._process_id = process_id
        self._process_name = process_name
        self._config = Config(self._mode, config_path)
        self._file = File(process_name, self._config)
        self._logger = logger or self._get_logger()

    def _get_logger(self) -> BaseLogger:
        return ProcessLogger(mode=self.mode,
                             config=self._config,
                             process_name=self._process_name,
                             job_id=self._job_id,
                             process_id=self._process_id)
