from pathlib import Path
from typing import Any, Optional

from ..exceptions import DirectoryNotFoundError, ProcessError
from ..logging.loggers import BaseLogger
from ..objects import Object, factory


class BaseDirectoryManager(object):
    _name = "Base"

    def __init__(self,
                 process_name: Optional[str],
                 base_path: str,
                 job_id: str,
                 logger: Optional[BaseLogger],
                 debug_mode: bool = False):
        self._process_name = process_name
        if base_path is None:
            self._base_path = None
        else:
            self._base_path = Path(base_path)
            self._base_path = self._base_path.joinpath(job_id)

        self._job_id = job_id
        self._logger = logger
        self._debug_mode = debug_mode

    def _check_base_path(self):
        if self._base_path is None:
            raise ProcessError(message="Base directory is not set",
                               detail="",
                               how_to_solve="",
                               reference_url="")
        if not self._base_path.exists():
            raise DirectoryNotFoundError(
                self._base_path,
                detail="{} directory should be placed on {}".format(self._name,
                                                                    str(self._base_path.resolve())),
                how_to_solve="Create directory on " + str(self._base_path.resolve()) +
                " or set proper path on config file",
                reference_url="")

    def get(self, file_name: str) -> Path:
        self._check_base_path()
        return self._base_path.joinpath(file_name)

    def get_object(self, name: str) -> Optional[Object]:
        path = self.get(name)
        if not path.exists():
            return None

        return factory(path)

    def directory(self) -> Path:
        return self._base_path

    def save_as_text(self, name: str, data: str) -> Path:
        self._check_base_path()
        path = self.get(name)
        path.write_text(data)
        return path

    def save_as_json(self, name: str, data: Any) -> Path:
        self._check_base_path()
        path = self.get(name)
        path.write_text(data)
        return path

    def save_from_object(self, _object: Object, file_name: str):
        path = self.get(file_name)
        _object.save(path)
