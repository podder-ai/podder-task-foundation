import logging
import time
from typing import Dict, Optional

from podder_task_foundation.config import Config

from .base_logger import BaseLogger


class ProcessLogger(BaseLogger):
    def __init__(self,
                 mode: str,
                 config: Config,
                 process_name: str,
                 job_id: Optional[str] = None,
                 process_id: Optional[str] = None,
                 logger: Optional[logging.Logger] = None):
        super().__init__(mode=mode, config=config, job_id=job_id, logger=logger)
        self._process_name = process_name
        self._process_id = process_id
        self._start_task()

    def _start_task(self):
        self._start_time = time.time()
        log_format = self.setting["task_log_format"]
        color_log_format = self.setting["color_task_log_format"]
        log_level = self.setting["task_log_level"]
        self._configure_logger(log_format, color_log_format, log_level)

    def _create_extra(self) -> Dict:
        extra = {
            'progresstime': str(round((time.time() - self._start_time), 3)),
            'processname': str(self._process_name),
            'jobid': str(self._job_id or ""),
            'processid': str(self._process_id or "")
        }
        return extra
