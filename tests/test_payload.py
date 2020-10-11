from podder_task_foundation import Payload
from pathlib import Path


def test_payload_create():
    payload = Payload()
    assert payload


def test_payload_load_image():
    payload = Payload()
    payload.add_file(Path(__file__).parent.joinpath("data", "test.png"))

    image = payload.get_image()
    assert image


def test_payload_load_json_dictionary():
    payload = Payload()
    payload.add_file(Path(__file__).parent.joinpath("data", "test_dictionary.json"))

    json_data = payload.get_data()
    assert json_data
    assert json_data["key"] == "value"


def test_payload_load_json_array():
    payload = Payload()
    payload.add_file(Path(__file__).parent.joinpath("data", "test_array.json"))

    json_data = payload.get_data()
    assert json_data
    assert json_data[1] == "value_1"


def test_payload_load_named_image():
    payload = Payload()
    payload.add_file(Path(__file__).parent.joinpath("data", "test.png"), name="test")

    image = payload.get_image()
    assert image

    image = payload.get_image("test")
    assert image

    image = payload.get_image("another")
    assert not image
