from podder_task_foundation import Parameters


def test_empty_parameters_create():
    parameter = Parameters({})

    assert parameter


def test_parameters_create():
    parameter = Parameters({"param01": "123", "param02": [1, 2, 3], "param03": 123})

    assert parameter


def test_parameters_all():
    parameter = Parameters({"param01": "123", "param02": [1, 2, 3], "param03": 123})

    _all = parameter.all()
    assert "param01" in _all


def test_parameters_has():
    parameter = Parameters({"param01": "123", "param02": [1, 2, 3], "param03": 123})

    assert parameter.has("param01")
    assert not parameter.has("param04")


def test_parameters_get():
    parameter = Parameters({"param01": "123", "param02": [1, 2, 3], "param03": 123})

    assert parameter.param01 == "123"
    assert parameter["param03"] == 123
    assert parameter.get("param03") == 123
    assert parameter.get("param04", "bbb") == "bbb"


def test_parameters_create_from_array():
    parameter = Parameters.from_cli_params(["--param01", "123", "--bool", "--array", "123", "456"])

    assert parameter
    assert parameter.param01 == "123"
    assert parameter.bool
    assert isinstance(parameter.get("array"), list)
    assert parameter["array"][1] == "456"
    assert parameter.has("bool")
