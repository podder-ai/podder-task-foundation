import copy
from typing import Any, Dict, List


class Parameters(object):
    __slots__ = ('_parameters', )

    def __init__(self, parameters: Dict[str, Any]):
        self._parameters = parameters

    def __getattr__(self, _name: str):
        if _name in self._parameters:
            return copy.deepcopy(self._parameters[_name])

        raise AttributeError("'Parameters' object has no attribute '{}'".format(_name))

    def __getitem__(self, key: str):
        if key in self._parameters:
            return copy.deepcopy(self._parameters[key])

        raise KeyError

    def __str__(self):
        return str(self._parameters)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        for key in self._parameters.keys():
            yield key, self._parameters[key]

    def get(self, key: str, default: Any = None):
        if key in self._parameters:
            return copy.deepcopy(self._parameters[key])

        return default

    def has(self, key: str) -> bool:
        return key in self._parameters

    def all(self) -> dict:
        return copy.deepcopy(self._parameters)

    def extend(self, additional_parameters: dict):
        self._parameters.update(additional_parameters)

    @classmethod
    def from_cli_params(cls, parameters: List[str]) -> "Parameters":
        dict_parameters = {}
        key_name = None
        value = None
        for parameter in parameters:
            if parameter.startswith("-"):
                if key_name is not None:
                    if value is None:
                        value = True
                    dict_parameters[key_name] = value
                    value = None
                key_name = parameter.lstrip("-")
            elif key_name is not None:
                print(parameter)
                if value is None:
                    value = parameter
                elif isinstance(value, list):
                    value.append(parameter)
                else:
                    value = [value, parameter]

        if key_name is not None:
            if value is None:
                value = True
            dict_parameters[key_name] = value

        return cls(dict_parameters)
