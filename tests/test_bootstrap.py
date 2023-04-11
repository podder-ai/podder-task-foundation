from pathlib import Path

from podder_task_foundation import MODE, Context, bootstrap


def test_bootstrap_execute():
    context = Context(mode=MODE.TEST, config_path=Path(__file__).parent.joinpath("data", "config"))
    result = bootstrap(context)
    assert result
