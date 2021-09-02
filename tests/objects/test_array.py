from collections import OrderedDict
from pathlib import Path

from podder_task_foundation.objects import Array, factory


def test_array_load():
    _object = factory(Path(__file__).parent.parent.joinpath("data", "array_01.json"))
    assert _object.type == "array"

    file_name = _object.get_file_name()
    assert file_name.name == "array_01.json"


def test_array_create():
    _object = Array(data=[1, 2, "123"])
    assert _object.type == "array"


def test_array_output_json_without_indent():
    _object = Array(data=[1, 2, "123"])
    json = _object.to_json()
    assert json == "[1, 2, \"123\"]"


def test_array_output_json_with_indent_2():
    _object = Array(data=[1, 2, "123"])
    json = _object.to_json(indent=2)
    assert json == "[\n  1,\n  2,\n  \"123\"\n]"


def test_array_output_json_with_indent_4():
    _object = Array(data=[1, 2, "123"])
    json = _object.to_json(indent=4)
    assert json == "[\n    1,\n    2,\n    \"123\"\n]"
