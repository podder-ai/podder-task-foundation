from collections import OrderedDict
from pathlib import Path

from podder_task_foundation.objects import Dictionary, factory


def test_dictionary_load():
    _object = factory(Path(__file__).parent.parent.joinpath("data", "dictionary_01.json"))
    assert _object.type == "dictionary"

    file_name = _object.get_file_name()
    assert file_name.name == "dictionary_01.json"


def test_dictionary_create():
    _object = Dictionary(data={"a": "b", "c": 123})
    assert _object.type == "dictionary"


def test_dictionary_output_json_without_indent():
    _object = Dictionary(data={"a": "b", "c": 123})
    json = _object.to_json()
    assert json == "{\"a\": \"b\", \"c\": 123}"


def test_dictionary_output_json_with_indent_2():
    _object = Dictionary(data={"a": "b", "c": 123})
    json = _object.to_json(indent=2)
    assert json == "{\n  \"a\": \"b\",\n  \"c\": 123\n}"


def test_dictionary_output_json_with_indent_4():
    _object = Dictionary(data={"a": "b", "c": 123})
    json = _object.to_json(indent=4)
    assert json == "{\n    \"a\": \"b\",\n    \"c\": 123\n}"


def test_dictionary_output_yaml_without_indent():
    _object = Dictionary(data={"a": "b", "c": 123})
    yaml = _object.to_yaml()
    assert yaml == "a: b\nc: 123\n"
