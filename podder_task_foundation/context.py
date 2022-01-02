import copy
import importlib
import logging
from pathlib import Path
from typing import Dict, Optional, Union

from .config import Config, SharedConfig
from .data_bag import DataBag
from .file import File
from .logging.loggers import BaseLogger, ProcessLogger
from .parameters import Parameters
from .utilities import UID, ProcessManager


class Context(object):
    @classmethod
    def copy(cls, process_name: Optional[str], parameters: Optional[Parameters],
             original: "Context") -> "Context":

        return cls(mode=original.mode,
                   process_name=process_name,
                   config_path=original.config_path,
                   logger=original.logger,
                   job_id=original.job_id,
                   process_id=None,
                   debug_mode=original.debug_mode,
                   verbose=original.verbose,
                   parameters=parameters,
                   custom_data=copy.deepcopy(original.custom_data.get()))

    @property
    def config(self) -> Config:
        return self._config

    @property
    def shared_config(self) -> SharedConfig:
        return self._shared_config

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
    def processes(self) -> [str]:
        return self._process_manager.get_process_list()

    @property
    def logger(self) -> BaseLogger:
        return self._logger

    @property
    def debug_mode(self) -> bool:
        return self._debug_mode

    @property
    def verbose(self) -> bool:
        return self._verbose

    @property
    def is_process_context(self) -> bool:
        return self._process_name is not None

    @property
    def version(self) -> str:
        return self._version

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @property
    def config_path(self) -> Optional[Path]:
        return self._config_path

    @property
    def custom_data(self) -> DataBag:
        return self._custom_data

    def __init__(self,
                 mode: str,
                 process_name: Optional[str] = None,
                 config_path: Optional[Path] = None,
                 logger: Union[BaseLogger, logging.Logger, None] = None,
                 job_id: Optional[str] = None,
                 process_id: Optional[str] = None,
                 debug_mode: bool = False,
                 verbose: bool = False,
                 parameters: Parameters = None,
                 custom_data: Optional[Dict] = None) -> None:
        self._mode = mode
        self._debug_mode = debug_mode
        self._verbose = verbose
        self._job_id = job_id or UID.generate()
        self._process_id = process_id or UID.generate()
        self._process_name = process_name
        self._config_path = config_path
        self._shared_config = SharedConfig(self._mode, path=config_path)
        self._process_manager = ProcessManager(self.mode, self._shared_config, self.debug_mode)
        self._custom_data = DataBag(custom_data)

        if parameters is None:
            self._parameters = Parameters({})
        else:
            self._parameters = parameters

        if self._process_name is not None:
            self._config = self._process_manager.get_process_config(self._process_name)
        else:
            self._config = self._shared_config

        if isinstance(logger, BaseLogger):
            self._logger = logger
        else:
            self._logger = self._get_logger(logger)
        self._file = File(process_name=process_name,
                          config=self._config,
                          job_id=self._job_id,
                          logger=self._logger,
                          debug_mode=debug_mode)
        self._version = self._get_version()
        self._process_list = self._process_manager.get_process_list()

    def _get_logger(self, logger: Optional[logging.Logger] = None) -> BaseLogger:
        return ProcessLogger(mode=self.mode,
                             config=self._config,
                             process_name=self._process_name,
                             job_id=self._job_id,
                             process_id=self._process_id,
                             logger=logger)

    def _get_version(self) -> str:
        __UNKNOWN = "unknown"
        if self._process_name is not None:
            try:
                process_module = importlib.import_module("processes.{}".format(self._process_name))
                return process_module.__version__
            except ModuleNotFoundError:
                return __UNKNOWN
            except AttributeError:
                return __UNKNOWN

        try:
            processes_module = importlib.import_module("processes")
            return processes_module.__version__
        except ModuleNotFoundError:
            return __UNKNOWN
        except AttributeError:
            return __UNKNOWN
