from collections import OrderedDict
from pathlib import Path

import pytest

from podder_task_foundation.objects import factory


@pytest.fixture
def data_path() -> Path:
    return Path(__file__).parent.parent.joinpath("data", "csv_01.csv")


def test_csv_create(data_path):
    _object = factory(data_path)
    assert _object.type == "array"

    file_name = _object.get_file_name()
    assert file_name.name == "csv_01.csv"


def test_csv_get_as_array(data_path):
    _object = factory(data_path)
    assert _object.type == "array"

    data = _object.data
    assert isinstance(data, list)
    assert isinstance(data[0], list)


def test_csv_get_as_dict(data_path):
    _object = factory(data_path)
    assert _object.type == "array"

    data = _object.get(data_format="dict")
    assert isinstance(data, list)
    print(type(data[0]))
    assert isinstance(data[0], dict)


def test_csv_get_data_after_get_as_dict(data_path):
    _object = factory(data_path)
    assert _object.type == "array"

    data = _object.get(data_format="dict")
    assert isinstance(data, list)
    assert isinstance(data[0], dict)

    data = _object.data
    assert isinstance(data, list)
    assert isinstance(data[0], list)
