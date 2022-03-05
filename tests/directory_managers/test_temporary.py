from pathlib import Path

import pytest

from podder_task_foundation.directory_managers.temporary import Temporary


@pytest.fixture
def temporary_path() -> str:
    return str(Path(__file__).parent.parent.joinpath("temporary").absolute())


def test_temporary_create(temporary_path: str):
    manager = Temporary(None, temporary_path, "jobid", logger=None, debug_mode=True)

    assert manager


def test_temporary_get(temporary_path: str):
    manager = Temporary(None, temporary_path, "jobid", logger=None, debug_mode=True)

    file = manager.get("test.json")
    assert file.exists()
