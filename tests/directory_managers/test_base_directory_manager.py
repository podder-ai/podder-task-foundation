from pathlib import Path

import pytest

from podder_task_foundation.directory_managers.base_directory_manager import BaseDirectoryManager


@pytest.fixture
def data_path() -> str:
    return str(Path(__file__).parent.parent.joinpath("data").absolute())


def test_base_directory_manager_create():
    manager = BaseDirectoryManager(None,
                                   str(Path(__file__).parent.parent.joinpath("data")),
                                   "jobid",
                                   logger=None,
                                   debug_mode=False)

    assert manager


def test_base_directory_manager_get(data_path: str):
    manager = BaseDirectoryManager(None, data_path, "jobid", logger=None, debug_mode=False)

    file = manager.get("array_01.json")
    assert file.exists()


def test_base_directory_manager_get_object(data_path: str):
    manager = BaseDirectoryManager(None, data_path, "jobid", logger=None, debug_mode=False)

    file = manager.get_object("array_01.json")
    assert file.type == "array"
