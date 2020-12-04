from pathlib import Path
from typing import Any, Optional

from ..exceptions import DirectoryNotFoundError
from ..logging.loggers import BaseLogger


class BaseDirectoryManager(object):
    _name = "Base"

    def __init__(self,
                 process_name: Optional[str],
                 base_path: str,
                 job_id: str,
                 logger: BaseLogger,
                 debug_mode: bool = False):
        self._process_name = process_name
        if base_path is None:
            self._base_path = None
        else:
            self._base_path = Path(base_path)
        self._job_id = job_id
        self._logger = logger
        self._debug_mode = debug_mode

    def _check_base_path(self):
        if not Path(self._base_path).exists():
            raise DirectoryNotFoundError(
                self._base_path,
                detail="{} directory should be placed on {}".format(self._name,
                                                                    str(self._base_path.resolve())),
                how_to_solve="Create directory on " + str(self._base_path.resolve()) +
                " or set proper path on config file",
                reference_url="")

    def get(self, name: str) -> Path:
        self._check_base_path()
        return self._base_path.joinpath(name)

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
