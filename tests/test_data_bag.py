from pathlib import Path

from podder_task_foundation import MODE, Context, DataBag, Process


def test_data_bag_create():
    data_bag = DataBag()
    assert data_bag


def test_data_bag_create_with_data():
    data_bag = DataBag({"test": "abc", "index": 12})

    assert data_bag


def test_data_bag_get_data():
    data_bag = DataBag({"test": "abc", "deep": {"test": "def"}})

    assert data_bag.get("test") == "abc"
    assert data_bag.get("deep.test") == "def"
    assert data_bag.get("deep.none", default="xyz") == "xyz"


def test_data_bag_set_data():
    data_bag = DataBag()
    data_bag.set("test", "abc")
    data_bag.set("deep.test", "def")

    assert data_bag.get("test") == "abc"
    assert data_bag.get("deep.test") == "def"
    assert data_bag.get("deep")["test"] == "def"
