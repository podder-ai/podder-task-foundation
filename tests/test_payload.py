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

    pdf_data = payload.get(object_type="file")
    assert pdf_data


def test_payload_load_directory():
    payload = Payload()
    payload.add_directory(Path(__file__).parent.joinpath("data"), name="directory")

    directory_data = payload.get(object_type="directory")
    assert directory_data


def test_payload_list_like_access():
    payload = Payload()
    payload.add_file(Path(__file__).parent.joinpath("data", "dictionary_01.json"))
    payload.add_file(Path(__file__).parent.joinpath("data", "pdf_01.pdf"))

    json_data = payload[0]
    assert json_data
    assert json_data["key"] == "value"

    pdf_data = payload[1]
    assert pdf_data.type == "file"

    list_payload = list(payload)
    assert len(list_payload) == 2
