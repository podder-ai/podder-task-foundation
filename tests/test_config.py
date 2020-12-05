from pathlib import Path

from podder_task_foundation import MODE, Context
from podder_task_foundation.config import Config


def test_config_create():
    config = Config(mode=MODE.TEST, path=Path(__file__).parent.joinpath("data", "config"))
    assert config


def test_get_value():
    config = Config(mode=MODE.TEST, path=Path(__file__).parent.joinpath("data", "config"))
    value = config.get("json.key")
    assert value == "value_shared"

    array = config.get("yaml.array")
    assert len(array) == 3


def test_get_from_context():
    context = Context(mode=MODE.TEST,
                      process_name="test",
                      config_path=Path(__file__).parent.joinpath("data", "config"))
    value = context.config.get("json.key")
    assert value == "value_process"


def test_get_shared_config_from_context():
    context = Context(mode=MODE.TEST,
                      process_name="test",
                      config_path=Path(__file__).parent.joinpath("data", "config"))
    value = context.shared_config.get("json.key")
    assert value == "value_shared"
