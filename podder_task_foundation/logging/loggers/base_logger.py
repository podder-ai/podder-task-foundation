import logging
import os
import sys
from typing import Dict, Optional

from colorlog import ColoredFormatter

from ...config import Config
from ..log_setting import LogSetting


class BaseLogger(object):
    TRACE_LOG_LEVEL = 5

    def __init__(self,
                 mode: str,
                 config: Config,
                 job_id: Optional[str],
                 logger: Optional[logging.Logger] = None):
        self._mode = mode
        self._config = config
        self._job_id = job_id
        self._add_trace_level()
        self._logger = logger or self._get_logger()
        self.setting = LogSetting(mode, config, job_id).load()

    @staticmethod
    def _get_logger() -> Optional[logging.Logger]:
        logger = logging.getLogger("console")
        return logger

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

    def add_handler(self, handler: logging.StreamHandler):
        self._logger.addHandler(handler)

    @staticmethod
    def _convert_newline_character(msg: str) -> str:
        if not isinstance(msg, str):
            return msg

        old_character = '\n'
        new_character = '\\n'

        return msg.replace(old_character, new_character)

    def _add_trace_level(self):
        logging.addLevelName(self.TRACE_LOG_LEVEL, "TRACE")

    def _format(self, level, msg, extra=None, *args, **kwargs):
        if self._logger is None:
            return
        self._logger.log(level, self._convert_newline_character(msg), extra=extra, *args, **kwargs)

    def _create_extra(self) -> Dict:
        return {"jobid": str(self._job_id or '')}

    def _configure_logger(self, log_format: str, color_log_format: str, log_level):
        self._logger.setLevel(log_level)
        self._logger.propagate = False
        self._add_handler(log_format, color_log_format, log_level)

    def _add_handler(self, log_format: str, color_log_format: str, log_level):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        self._set_logger_formatter(handler, log_format, color_log_format)
        if self._logger.hasHandlers():
            self._logger.handlers.clear()
        self._logger.addHandler(handler)

    def _set_logger_formatter(self, handler: logging.StreamHandler, log_format: str,
                              color_log_format: str) -> None:
        date_format = self.setting['date_format']
        if self._support_color():
            color_formatter = self._get_color_formatter(color_log_format, date_format)
            handler.setFormatter(color_formatter)
        else:
            formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
            handler.setFormatter(formatter)

    def _get_color_formatter(self, log_format: str, date_format: str) -> ColoredFormatter:
        color_formatter = ColoredFormatter(
            fmt=log_format,
            datefmt=date_format,
            log_colors=self.setting["log_colors"],
            secondary_log_colors=self.setting["secondary_log_colors"])
        return color_formatter

    @staticmethod
    def _support_color() -> bool:
        platform = sys.platform
        supported_platform = \
            platform != 'Pocket PC' and (platform != 'win32' or 'ANSICON' in os.environ)
        if not supported_platform:
            return False

        for handle in [sys.stdout, sys.stderr]:
            is_a_tty = hasattr(handle, 'isatty') and handle.isatty()
            if not is_a_tty:
                return False

        return True
