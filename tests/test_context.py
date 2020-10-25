from pathlib import Path

from podder_task_foundation import MODE, Context, Payload, Process


def test_context_create():
    context = Context(mode=MODE.TEST, config_path=Path(__file__).parent.joinpath("data", "config"))
    assert context


def test_process_context_create():
    context = Context(mode=MODE.TEST,
                      process_name="test",
                      config_path=Path(__file__).parent.joinpath("data", "config"))
    assert context
