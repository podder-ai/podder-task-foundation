import logging
import os
from typing import Any, Dict

from podder_task_foundation.config import Config


class LogSetting:
    TASK_NAME_PATH = 'task_name.ini'
    DEFAULT_FORMAT = '[%(asctime)s.%(msecs)03d] %(levelname)s - %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    _log_setting = None

    def __init__(self, mode: str, config: Config):
        self._mode = mode
        self._config = config

    def load(self):
        if LogSetting._log_setting is None:
            LogSetting._log_setting = self._load_log_yml()
        return LogSetting._log_setting

    def _get_config(self, key: str, default: Any) -> Any:
        value = self._config.get("log." + key)
        if value is not None:
            return value
        value = self._config.get("pipeline." + key)
        if value is not None:
            return value

        return default

    def _load_log_yml(self) -> Dict:
        if os.path.exists(self.TASK_NAME_PATH):
            with open(self.TASK_NAME_PATH, 'r') as stream:
                task_name = stream.read()
        else:
            task_name = self._get_config('app.name', '')

        settings = {
            'task_name': task_name,
            'default_log_format': self.DEFAULT_FORMAT,
            'date_format': self.DATE_FORMAT,
            'task_log_format': self._get_config('task_log_format', self.DEFAULT_FORMAT),
            'server_log_format': self._get_config('server_log_format', self.DEFAULT_FORMAT),
            'color_task_log_format': self._get_config('color_task_log_format', self.DEFAULT_FORMAT),
            'color_server_log_format': self._get_config('color_server_log_format',
                                                        self.DEFAULT_FORMAT),
            'task_log_level': self._get_config('task_log_level', logging.DEBUG),
            'server_log_level': self._get_config('server_log_level', logging.DEBUG),
            'log_colors': self._get_config('log_colors', {}),
            'secondary_log_colors': self._get_config('secondary_log_colors', {}),
        }

        return settings
