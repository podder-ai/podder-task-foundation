import logging
import sys
import traceback
from typing import Any, Optional

from .context import Context
from .exceptions import ProcessError
from .logging.stream_to_logger import StreamToLogger
from .payload import Payload


class Process(object):
    def __init__(self, mode: str, context: Optional[Context] = None) -> None:
        if context is None:
            context = Context(mode, self._get_process_name())
        self.context = context
        self.initialize(context)

    def _get_process_name(self) -> str:
        module = self.__class__.__module__

        if module is None or module == str.__class__.__module__:
            full_name = self.__class__.__name__
        else:
            full_name = module + '.' + self.__class__.__name__

        elements = full_name.split(".")
        if len(elements) < 2:
            raise ProcessError(
                message="Your Process class is placed on different place {}.".format(full_name),
                detail="It should placed on ./processes/[your task name]/process.py",
                how_to_solve="Move your Process class to the right place",
            )

        return elements[-2]

    def initialize(self, context: Context) -> None:
        pass

    def handle(self, input_: Optional[Payload] = None) -> Payload:
        output = Payload()

        logger = self.context.logger
        sys.stdout = StreamToLogger(logger)
        sys.stderr = StreamToLogger(logger, log_level=logging.ERROR)

        try:
            self.execute(input_, output, self.context)
        except ProcessError as exception:
            self.context.logger.critical(exception.message)
            self.context.logger.critical("".join(
                traceback.format_exception(etype=Exception, value=exception, tb=None)))
        except SystemExit:
            self.context.logger.critical("system exit")
            raise Exception
        except KeyboardInterrupt as exception:
            raise exception


#        except Exception as exception:
#            self.context.logger.error("".join(traceback.format_exception()))

        return output

    def execute(self, input_payload: Payload, output_payload: Payload, context: Context):
        pass
