from pathlib import Path

import pytest

from podder_task_foundation.objects import factory


@pytest.fixture
def data_path() -> Path:
    return Path(__file__).parent.parent.joinpath("data", "dictionary_01.json")


def test_array_create(data_path):
    _object = factory(data_path)
    assert _object.type == "dictionary"

    file_name = _object.get_file_name()
    assert file_name.name == "dictionary_01.json"


def test_array_data_retrieval(data_path):
    _object = factory(data_path)
    data = _object.data
    assert isinstance(data, dict)
    assert data["key"] == "value"
