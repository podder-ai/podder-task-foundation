import os
from pathlib import Path

from .config import Config
from .directory_managers import Data, Input, Output, Temporary
from .exceptions import DirectoryNotFoundError
from .logging.loggers import BaseLogger


class File(object):
    """
    File assessor
    All tasks need to access file through this class
    """
    def __init__(self,
                 process_name: str,
                 config: Config,
                 job_id: str,
                 logger: BaseLogger,
                 debug_mode: bool = False):
        self._process_name = process_name
        self._config = config
        self._job_id = job_id
        self._logger = logger
        self._debug_mode = debug_mode
        self._root_path = os.path.abspath(config.get('file.root_directory', './'))
        self._temporary_directory = self._get_temporary_directory()
        self._data_directory = self._get_data_directory()
        self._input_directory = self._get_input_directory()
        self._output_directory = self._get_output_directory()

    def _get_temporary_directory(self) -> Temporary:
        if self._debug_mode:
            base_path = self._config.get('file.debug.temporary_directory',
                                         os.path.join(self.get_root_path(), 'temp'))
        else:
            base_path = self._config.get('file.temporary_directory', None)

        return Temporary(process_name=self._process_name,
                         base_path=base_path,
                         job_id=self._job_id,
                         logger=self._logger,
                         debug_mode=self._debug_mode)

    def _get_input_directory(self) -> Input:
        directory_path = self._config.get('file.input_directory',
                                          os.path.join(self.get_root_path(), 'input'))
        return Input(process_name=self._process_name,
                     base_path=directory_path,
                     job_id=self._job_id,
                     logger=self._logger,
                     debug_mode=self._debug_mode)

    def _get_output_directory(self) -> Output:
        directory_path = self._config.get('file.output_directory',
                                          os.path.join(self.get_root_path(), 'output'))
        return Output(process_name=self._process_name,
                      base_path=directory_path,
                      job_id=self._job_id,
                      logger=self._logger,
                      debug_mode=self._debug_mode)

    def _get_data_directory(self) -> Data:
        directory_path = self._config.get('file.data_directory',
                                          os.path.join(self.get_root_path(), 'data'))
        return Data(process_name=self._process_name,
                    base_path=directory_path,
                    job_id=self._job_id,
                    logger=self._logger,
                    debug_mode=self._debug_mode)

    @property
    def temporary_directory(self) -> Temporary:
        return self._temporary_directory

    @property
    def input_directory(self) -> Input:
        return self._input_directory

    @property
    def output_directory(self) -> Output:
        return self._output_directory

    @property
    def data_directory(self) -> Data:
        return self._data_directory

    def get_root_path(self) -> str:
        return self._root_path

    def get_input_path(self, name: str = '') -> str:
        return str(self.get_input_file(name))

    def get_output_path(self, name: str = '') -> str:
        return str(self.get_output_file(name))

    def get_data_path(self, name: str = '') -> str:
        return str(self.get_data_file(name))

    def get_temporary_path(self, name: str) -> str:
        return str(self.get_temporary_file(name))

    def get_input_file(self, name: str) -> Path:
        return self._input_directory.get(name)

    def get_output_file(self, name: str) -> Path:
        return self._output_directory.get(name)

    def get_data_file(self, name: str) -> Path:
        return self._data_directory.get(name)

    def get_temporary_file(self, name: str) -> Path:
        return self._temporary_directory.get(name)
