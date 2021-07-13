from pathlib import Path

from podder_task_foundation import Payload


def test_payload_create():
    payload = Payload()
    assert isinstance(payload, Payload)


def test_payload_load_json_dictionary():
    payload = Payload()
    payload.add_file(Path(__file__).parent.joinpath("data", "dictionary_01.json"))

    json_data = payload.get_data()
    assert json_data
    assert json_data["key"] == "value"


def test_payload_load_json_array():
    payload = Payload()
    payload.add_file(Path(__file__).parent.joinpath("data", "array_01.json"))

    json_data = payload.get_data()
    assert json_data
    assert json_data[1] == "value_1"


def test_payload_load_pdf():
    payload = Payload()
    payload.add_file(Path(__file__).parent.joinpath("data", "pdf_01.pdf"))

    pdf_data = payload.get(object_type="pdf")
    assert pdf_data


def test_payload_load_directory():
    payload = Payload()
    payload.add_directory(Path(__file__).parent.joinpath("data"))

    objects = payload.all()
    assert len(objects) == 6
    assert objects[0].type == "array"
    assert objects[0].name == "array_01.json"
    assert objects[0].extension == ".json"
