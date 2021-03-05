from csv import DictReader
import json
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Union

import toml
import yaml

from ..exceptions import UnsupportedFileFormatError


def represent_odict(dumper, instance):
    return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())


yaml.add_representer(OrderedDict, represent_odict)


class DataFileLoader(object):
    supported_format = {
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".csv": "csv",
    }

    def __init__(self):
        pass

    def load(self, path: Path, encoding: Optional[str] = 'utf-8') -> Union[Dict, List]:
        file_format = self.get_file_type(path)
        if file_format is None:
            raise UnsupportedFileFormatError(path)
        data = None
        if file_format == "json":
            data = json.loads(path.read_text(encoding=encoding), object_pairs_hook=OrderedDict)
        elif file_format == "yaml":
            data = yaml.load(path.read_text(encoding=encoding), Loader=yaml.SafeLoader)
        elif file_format == "toml":
            data = toml.loads(path.read_text(encoding=encoding), _dict=OrderedDict)
        elif file_format == "csv":
            data = []
            with open(path, encoding=encoding) as read_object:
                dict_object = DictReader(read_object)
                data = list(dict_object)

        return data

    def get_file_type(self, path: Path) -> Optional[str]:
        if path.suffix not in self.supported_format.keys():
            return None
        return self.supported_format[path.suffix]
