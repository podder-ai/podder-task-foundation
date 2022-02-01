from collections import OrderedDict
from pathlib import Path

import pytest

from podder_task_foundation.objects import Directory, factory


@pytest.fixture
def data_path() -> Path:
    return Path(__file__).parent.parent.joinpath("data", "directory")


def test_directory_load(data_path):
    _object = factory(data_path)
    assert _object.type == "directory"

    file = _object.get_file("test.json")
    assert file.exists()


def test_directory_create(data_path):
    _object = Directory()
    assert _object.type == "directory"

    path = _object.path
    assert path.exists()
    assert path.is_dir()


def test_directory_create_with_name(data_path):
    _object = Directory(name="name")
    assert _object.type == "directory"

    path = _object.path
    assert path.exists()
    assert path.is_dir()


def test_directory_create_with_directory_and_destroy(data_path):
    _object = Directory(data=data_path)
    assert _object.type == "directory"
    del _object
