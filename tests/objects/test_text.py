from pathlib import Path

import pytest

from podder_task_foundation.objects import Text, factory


@pytest.fixture
def data_path() -> Path:
    return Path(__file__).parent.parent.joinpath("data", "text_01.txt")


def test_text_create(data_path):
    _object = factory(data_path)
    assert _object.type == "text"

    file_name = _object.get_file_name()
    assert file_name.name == "text_01.txt"


def test_text_get_as_string(data_path):
    _object = factory(data_path)
    data = _object.data
    assert isinstance(data, str)


def test_text_get_as_list(data_path):
    _object = factory(data_path)

    assert isinstance(_object, Text)
    data = _object.to_array()

    assert len(data) == 3
