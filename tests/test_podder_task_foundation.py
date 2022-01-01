from pathlib import Path

import toml

from podder_task_foundation import __version__


def test_version():
    file = Path(__file__).parent.parent.joinpath("pyproject.toml")
    data = toml.loads(file.read_text(encoding="utf-8"))

    if "tool" in data and "poetry" in data["tool"] and "version" in data["tool"]["poetry"]:
        project_version = data["tool"]["poetry"]["version"]
        assert __version__ == project_version
