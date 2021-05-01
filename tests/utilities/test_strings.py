from podder_task_foundation.utilities import Strings


def test_instance_create():
    instance = Strings()
    assert instance is not None


def test_camel_case():
    instance = Strings()
    source = "test_case"
    title = instance.camel_case(source, False)
    assert title == "testCase"

    title = instance.camel_case(source, True)
    assert title == "TestCase"
