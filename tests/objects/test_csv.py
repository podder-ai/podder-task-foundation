from collections import OrderedDict
from pathlib import Path

from podder_task_foundation.objects import CSV, factory


def test_csv_create():
    _object = factory(Path(__file__).parent.parent.joinpath("data", "csv_01.csv"))
    assert _object.type == "csv"

    file_name = _object.get_file_name()
    assert file_name.name == "csv_01.csv"


def test_csv_get_as_array():
    _object = factory(Path(__file__).parent.parent.joinpath("data", "csv_01.csv"))
    assert _object.type == "csv"

    data = _object.data
    assert isinstance(data, list)
    assert isinstance(data[0], list)


def test_csv_get_as_dict():
    _object = factory(Path(__file__).parent.parent.joinpath("data", "csv_01.csv"))
    assert _object.type == "csv"

    data = _object.get_data(data_format="dict")
    assert isinstance(data, list)
    assert isinstance(data[0], OrderedDict)


def test_csv_get_data_after_get_as_dict():
    _object = factory(Path(__file__).parent.parent.joinpath("data", "csv_01.csv"))
    assert _object.type == "csv"

    data = _object.get_data(data_format="dict")
    assert isinstance(data, list)
    assert isinstance(data[0], OrderedDict)

    data = _object.data
    assert isinstance(data, list)
    assert isinstance(data[0], list)
