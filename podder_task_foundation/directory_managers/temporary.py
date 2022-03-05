import tempfile
from pathlib import Path
from typing import Optional

from ..exceptions import DirectoryNotFoundError
from ..logging.loggers import BaseLogger
from .base_directory_manager import BaseDirectoryManager


class Temporary(BaseDirectoryManager):
    _name = "Temporary"

    def __init__(self,
                 process_name: Optional[str],
                 base_path: Optional[str],
                 job_id: str,
                 logger: Optional[BaseLogger],
                 debug_mode: bool = False):
        super().__init__(process_name, base_path, job_id, logger, debug_mode)
        if base_path is not None:
            self._base_path = Path(base_path).joinpath(job_id)

        self._base_root_path = self._base_path
        self._temporary_directory_object: Optional[tempfile.TemporaryDirectory] = None
        self._base_path = None
        self._create_temporary_file()

    def __del__(self):
        if self._temporary_directory_object is not None:
            self._temporary_directory_object.cleanup()

    def _check_base_path(self):
        if not self._debug_mode:
            if self._base_root_path is not None and not Path(self._base_root_path).exists():
                raise DirectoryNotFoundError(self._base_path,
                                             detail="{} directory should be placed on {}".format(
                                                 self._name, str(self._base_path.resolve())),
                                             how_to_solve="Create directory on " +
                                             str(self._base_path.resolve()) +
                                             " or set proper path on config file",
                                             reference_url="")

        if not Path(self._base_path).exists():
            Path(self._base_path).mkdir(parents=True)

    def _create_temporary_file(self) -> None:
        if self._debug_mode:
            if self._process_name:
                self._base_path = self._base_root_path.joinpath(self._process_name)
            else:
                self._base_path = self._base_root_path
            if self._logger:
                self._logger.debug(
                    "Create temporary directory for debugging ( won't be deleted ): {}".format(
                        self._base_path.absolute()))
        else:
            self._temporary_directory_object = tempfile.TemporaryDirectory(prefix=self._job_id,
                                                                           dir=self._base_root_path)
            self._base_path = Path(self._temporary_directory_object.name)
            if self._logger:
                self._logger.debug("Create temporary directory: {}".format(
                    self._base_path.absolute()))
