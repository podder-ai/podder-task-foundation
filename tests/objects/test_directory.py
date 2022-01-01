from collections import OrderedDict
from pathlib import Path

import pytest

from podder_task_foundation.objects import factory


@pytest.fixture
def data_path() -> Path:
    return Path(__file__).parent.parent.joinpath("data", "directory")


def test_directory_load(data_path):
    _object = factory(data_path)
    assert _object.type == "directory"

    file = _object.get_file("test.json")
    assert file.exists()
