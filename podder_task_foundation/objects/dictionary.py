import json
from collections import OrderedDict
from pathlib import Path

from podder_task_foundation.utilities import DataFileLoader

from .text_serializable import TextSerializable


class Dictionary(TextSerializable):
    _properties = OrderedDict({})
    type = "dictionary"

    def __getattr__(self, item):
        if item not in self.data.keys():
            raise AttributeError("'{}' object has no attribute '{}'".format(
                type(self).__name__, item))
        return self.data[item]

    def __contains__(self, item):
        return item in self.data.keys()

    @classmethod
    def is_supported_file(cls, path: Path) -> bool:
        if path.suffix not in cls.supported_extensions:
            return False

        with path.open() as file:
            data = file.read(64)
        data = data.strip()

        file_type = DataFileLoader().get_file_type(path)
        if file_type is None:
            return False

        if file_type == "json":
            if data[0] == "{":
                return True

        if file_type == "yaml":
            data = data.strip()
            if data[0] != "-":
                return True

        return False
