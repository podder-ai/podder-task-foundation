import logging
from pathlib import Path

from podder_task_foundation import MODE, Context, Payload, Process


def test_logger_create():
    context = Context(mode=MODE.TEST, config_path=Path(__file__).parent.joinpath("data", "config"))
    assert context
    assert context.logger


def test_logger_add_handler():
    context = Context(mode=MODE.TEST, config_path=Path(__file__).parent.joinpath("data", "config"))
    assert context
    assert context.logger
    before_handler_number = len(context.logger._logger.handlers)
    null_handler = logging.NullHandler()
    context.logger.add_handler(null_handler)
    assert len(context.logger._logger.handlers) == before_handler_number + 1
