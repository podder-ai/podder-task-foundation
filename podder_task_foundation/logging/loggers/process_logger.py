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
                 process_id: Optional[str] = None):
        super().__init__(mode, config, job_id)
        self._process_name = process_name
        self._process_id = process_id
        self._start_task()

    def _start_task(self):
        self._start_time = time.time()
        log_format = self.setting["task_log_format"]
        color_log_format = self.setting["color_task_log_format"]
        log_level = self.setting["task_log_level"]
        self._configure_logger(log_format, color_log_format, log_level)

    def trace(self, msg, *args, **kwargs):
        self._format(self.TRACE_LOG_LEVEL, msg, extra=self._create_extra(), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._format(logging.DEBUG, msg, extra=self._create_extra(), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._format(logging.INFO, msg, extra=self._create_extra(), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._format(logging.WARNING, msg, extra=self._create_extra(), *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self._format(logging.WARNING, msg, extra=self._create_extra(), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._format(logging.ERROR, msg, extra=self._create_extra(), *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self._format(logging.ERROR, msg, extra=self._create_extra(), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._format(logging.CRITICAL, msg, extra=self._create_extra(), *args, **kwargs)

    def _create_extra(self) -> Dict:
        extra = {
            'progresstime': str(round((time.time() - self._start_time), 3)),
            'processname': str(self._process_name),
            'jobid': str(self._job_id or ""),
            'processid': str(self._process_id or "")
        }
        return extra
