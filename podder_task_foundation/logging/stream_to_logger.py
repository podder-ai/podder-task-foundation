import logging


class StreamToLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self._logger = logger
        self._log_level = log_level

    def write(self, message):
        for line in message.rstrip().splitlines():
            if self._log_level == logging.INFO:
                self._logger.info(line.rstrip())
            if self._log_level == logging.ERROR:
                self._logger.error(line.rstrip())

    def flush(self):
        pass
